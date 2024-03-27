"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

# pylint: disable=arguments-differ
from copy import deepcopy
from typing import List

import numpy as np
from onnx import mapping
from onnx.helper import (
    make_node,
    make_tensor_type_proto,
    make_tensor_value_info,
    make_value_info,
)
from onnx.onnx_pb import NodeProto

from onnx2onnx.graph import OnnxGraph

from . import PASSES
from .pattern import GraphPattern, SingleNodePattern
from .rewriter import Rewriter
from .utils import make_constant


@PASSES.register(name="reorder_quantizelinear")
class ReorderQuantizeLinearRewriter(Rewriter):
    """Reorder X - Q - DQ pattern to Q - X - DQ where X match the following pattern:

    - `X` has no parameter variables (such as Conv, MatMul, etc.)
    - `X` doesn't change channels when Q-DQ is channel-wise

    Example::

        Before:

            SpaceToDepth - QuantizeLinear - DequantizeLinear

        After:

            QuantizeLinear - SpaceToDepth - DequantizeLinear
    """

    _ALLOW_X_TYPES = {"SpaceToDepth", "DepthToSpace", "MaxPool", "AveragePool"}

    def __init__(self):
        pattern = GraphPattern()
        p1 = SingleNodePattern("QuantizeLinear")
        p2 = SingleNodePattern("DequantizeLinear")
        pattern.add_edge(p1, p2)
        super().__init__(pattern)

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        qnode, dqnode = nodes
        assert qnode.op_type == "QuantizeLinear"
        assert dqnode.op_type == "DequantizeLinear"

        upstream_nodes = graph.onnx_predecessors(qnode)
        if len(upstream_nodes) != 1:
            return  # not a single path

        xnode = upstream_nodes[0]
        if xnode.op_type not in self._ALLOW_X_TYPES:
            return  # not a valid X node

        qnode_new = deepcopy(qnode)
        qnode_new.name += f"/{self.__class__.__name__}"
        dqnode_new = deepcopy(dqnode)
        dqnode_new.name += f"/{self.__class__.__name__}"
        xnode_new = deepcopy(xnode)
        xnode_new.name += f"/{self.__class__.__name__}"

        # swap X input and Q input
        qnode_new.input[0], xnode_new.input[0] = xnode.input[0], qnode.output[0]
        dqnode_new.input[0] = xnode.output[0]

        self -= [xnode, qnode, dqnode]
        self += [xnode_new, qnode_new, dqnode_new]


@PASSES.register(name="space2depth_to_qconv")
class SpaceToDepthToQConvRewriter(Rewriter):
    """Convert SpaceToDepth - QDQ to quantized Conv."""

    def __init__(self):
        qdq_pattern = GraphPattern()
        s2d = SingleNodePattern("SpaceToDepth")
        qpattern = SingleNodePattern("QuantizeLinear")
        dqpattern = SingleNodePattern("DequantizeLinear")
        qdq_pattern.add_edge(s2d, qpattern)
        qdq_pattern.add_edge(qpattern, dqpattern)
        super().__init__(pattern=qdq_pattern)

    def _copy_qdq(self, node: NodeProto) -> NodeProto:
        axis = self.get_attribute(node, "axis") or 0
        scale_node = self.get_input_node(node, 1)
        scale_value = self.get_value(scale_node)
        new_scale = make_constant(node.name + "/scale/copy", scale_value)
        input_names = [node.input[0] + "/copy", new_scale.output[0]]
        if len(node.input) == 3:
            zero_node = self.get_input_node(node, 2)
            zero_value = self.get_value(zero_node)
            new_zero = make_constant(node.name + "/zero/copy", zero_value)
            self += new_zero
            input_names += new_zero.output[:]
        new_node = make_node(
            node.op_type,
            input_names,
            [o + "/copy" for o in node.output],
            node.name + "/s2d_to_qconv/copy",
            axis=axis,
        )
        self += [new_scale]
        return new_node

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        s2d, qnode, dqnode = nodes
        blocksize = self.get_attribute(s2d, "blocksize")
        _, ic, _, _ = graph.tensor_shape(s2d.input[0])
        _, oc, _, _ = graph.tensor_shape(s2d.output[0])
        etype = graph.tensor_type(dqnode.input[0])
        dtype = mapping.TENSOR_TYPE_MAP[etype].np_dtype
        assert ic * blocksize**2 == oc, "invalid space2depth parameters"

        qnode_ahead = self._copy_qdq(qnode)
        dqnode_ahead = self._copy_qdq(dqnode)
        qnode_ahead.input[0] = s2d.input[0]
        dqnode_ahead.input[0] = qnode_ahead.output[0]

        kernel = (
            # fmt: off
            np.tile(
                np.eye(blocksize**2)
                .reshape([-1, blocksize, blocksize])
                .astype(dtype),
                [ic, 1, 1, 1],
            )
            .transpose([1, 0, 2, 3])
            .reshape([oc, 1, blocksize, blocksize])
            # fmt: on
        )
        # expand to [oc, ic, blocksize, blocksize]
        kernel = np.concatenate(
            [kernel, np.tile(np.zeros_like(kernel), [1, ic - 1, 1, 1])], axis=1
        )
        for i in range(1, ic):
            kernel[i::ic][:, i] = kernel[i::ic][:, 0]
            kernel[i::ic][:, 0] = 0  # swap
        conv_weight = make_constant(name=f"{s2d.name}/weight", value=kernel)

        # kernel dequantize
        kernel_scale = make_constant(
            conv_weight.name + "/scale", np.ones([oc], np.float32)
        )
        kernel_zp = make_constant(conv_weight.name + "/zero", np.zeros([oc], dtype))
        kernel_dq = make_node(
            "DequantizeLinear",
            [conv_weight.output[0], kernel_scale.output[0], kernel_zp.output[0]],
            [conv_weight.output[0] + "/dq"],
            conv_weight.name + "/dequantize",
            axis=0,
        )

        conv = make_node(
            op_type="Conv",
            inputs=dqnode_ahead.output[:] + [kernel_dq.output[0]],
            outputs=s2d.output,
            name=f"{s2d.name}/conv",
            kernel_shape=[blocksize, blocksize],
            strides=[blocksize, blocksize],
        )
        self -= s2d
        self += [
            qnode_ahead,
            dqnode_ahead,
            kernel_dq,
            kernel_scale,
            kernel_zp,
            conv_weight,
            conv,
        ]


@PASSES.register(name="expand_qconv_channel", deps=["initializer_to_constant"])
class ExpandQConvChannelRewriter(Rewriter):
    """Expand QConv's channel to 4"""

    def __init__(self):
        pattern = GraphPattern()
        qpattern = SingleNodePattern("QuantizeLinear")
        dqpattern = SingleNodePattern("DequantizeLinear")
        conv = SingleNodePattern("Conv")
        pattern.add_edge(qpattern, dqpattern)
        pattern.add_edge(dqpattern, conv)
        super().__init__(pattern=pattern)

    def rewrite(self, graph: OnnxGraph, nodes: List):
        q_node, _, conv_node = nodes
        n, ic, h, w = graph.tensor_shape(conv_node.input[0])
        if ic != 3:
            return
        old_inputs = list(filter(lambda x: x.name == q_node.input[0], graph.input))
        if len(old_inputs) != 1:
            return
        old_input = old_inputs[0]
        # make sure that only one node connects with the old_input
        # TODO: support that multiple ops use old_input
        nodes = list(
            filter(lambda x: old_input.name in x["pb"].input, graph.nodes.values())
        )
        if len(nodes) != 1:
            return
        # make sure that only one node connects with the old_input
        # TODO: support that multiple ops use old_input
        nodes = list(
            filter(lambda x: old_input.name in x["pb"].input, graph.nodes.values())
        )
        if len(nodes) != 1:
            return

        # expand weight
        weight_dq_node = self.get_input_node(conv_node, 1)
        weight_node = self.get_input_node(weight_dq_node, 0)
        weight_value = self.get_value(weight_node)
        oc, _, kh, kw = weight_value.shape
        expand_weight_value = np.zeros([oc, 4, kh, kw], dtype=weight_value.dtype)
        expand_weight_value[:, :3, :, :] = weight_value
        # set zero value by zero point
        zero_point_value = self.get_value(self.get_input_node(weight_dq_node, 2))
        expand_weight_value[:, 3, :, :] = np.reshape(zero_point_value, [oc, 1, 1])

        expand_weight_node = make_constant(
            weight_node.name + "/expand", expand_weight_value
        )

        # connect weight
        weight_dq_node.input[0] = expand_weight_node.output[0]
        # change input dim
        q_node.input[0] += "_expand"

        # replace graph input
        graph.input.append(
            make_value_info(q_node.input[0], make_tensor_type_proto(1, [n, 4, h, w]))
        )
        graph.input.remove(old_input)
        graph.inputs.pop(old_input.name)
        self -= weight_node
        self += expand_weight_node


@PASSES.register(name="merge_quantize_input")
class MergeQuantizeInputPass(Rewriter):
    """Merge QuantizeLinear into inputs and change input type to uint8.

    Example::

        Before:

            input{float32} - QuantizeLinear - DequantizeLinear

        After:

            input{uint8} - DequantizeLinear
    """

    def __init__(self):
        pattern = GraphPattern()
        qpattern = SingleNodePattern("QuantizeLinear")
        dqpattern = SingleNodePattern("DequantizeLinear")
        pattern.add_edge(qpattern, dqpattern)
        super().__init__(pattern=pattern)

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        qlinear, dqlinear = nodes
        if qlinear.input[0] not in graph.inputs:
            # only process the node after graph inputs
            return
        succ_nodes = graph.onnx_successors(qlinear)
        pred_nodes = graph.onnx_predecessors(qlinear)
        if len(succ_nodes) != 1 or succ_nodes[0].op_type != "DequantizeLinear":
            # double check
            return
        # quantized data type
        shape, qtype = graph.tensor_info(qlinear.output[0])
        # remove the original input
        old_inp = graph.input.pop(graph.inputs.pop(qlinear.input[0]))
        input_name = old_inp.name
        # keep input name unchanged
        dqlinear.input[0] = input_name
        graph.input.append(make_tensor_value_info(dqlinear.input[0], qtype, shape))
        graph.inputs[dqlinear.input[0]] = len(graph.input) - 1
        self -= qlinear
        self -= pred_nodes

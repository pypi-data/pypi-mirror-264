"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

from contextlib import suppress
from typing import List

import networkx as nx
import numpy as np
from onnx import NodeProto

from onnx2onnx.evaluator import Evaluator

from . import L1, L3, OnnxGraph
from .pattern import ConstantGraphPattern, SingleNodePattern
from .rewriter import Rewriter
from .utils import make_constant

with suppress(ImportError):
    import onnxoptimizer

    @L3.register()
    def onnx_optimizer(graph: OnnxGraph, passes: List[str] = None):
        """Fuse op and remove isolated nodes.

        Args:
            graph (OnnxGraph): The onnx graph to be optimized.
            passes (List[str], optional): The optimization passes to be applied.
                Defaults to None.
        """

        if not passes:
            passes = [
                "eliminate_nop_cast",
                "eliminate_nop_dropout",
                "eliminate_nop_flatten",
                "eliminate_if_with_const_cond",
                "eliminate_nop_monotone_argmax",
                "eliminate_nop_pad",
                "eliminate_nop_concat",
                "eliminate_nop_split",
                "eliminate_nop_expand",
                "eliminate_shape_gather",
                "eliminate_slice_after_shape",
                "eliminate_nop_reshape",
                "eliminate_nop_with_unit",
                "eliminate_common_subexpression",
                "eliminate_deadend",
                "eliminate_identity",
                "eliminate_shape_op",
                "eliminate_unused_initializer",
                "eliminate_duplicate_initializer",
                "fuse_add_bias_into_conv",
                "fuse_bn_into_conv",
                "fuse_concat_into_reshape",
                "fuse_consecutive_concats",
                "fuse_consecutive_log_softmax",
                "fuse_consecutive_reduce_unsqueeze",
                "fuse_consecutive_slices",
                "fuse_consecutive_squeezes",
                "fuse_consecutive_transposes",
                "fuse_consecutive_unsqueezes",
                "fuse_matmul_add_bias_into_gemm",
                "fuse_pad_into_conv",
                "fuse_pad_into_pool",
                "fuse_qkv",
                "fuse_transpose_into_gemm",
                "extract_constant_to_initializer",
            ]
        return OnnxGraph(onnxoptimizer.optimize(graph.model, passes))


with suppress(ImportError):
    import onnxsim

    @L3.register()
    def onnx_simplifier(graph: OnnxGraph):
        """Simplify onnx graph"""
        model_sim, succeed = onnxsim.simplify(graph.model)
        if succeed:
            return OnnxGraph(model_sim)
        return graph


@L1.register(
    name="fold_constant",
    deps=["initializer_to_constant", "infer_shape", "shape_to_constant"],
)
class FoldConstantPass(Rewriter):
    """Fold constants to a single node."""

    def __init__(self):
        super().__init__(pattern=ConstantGraphPattern())

    def _is_constant_or_qdq(self, node):
        return node.op_type in {"Constant", "DequantizeLinear", "QuantizeLinear"}

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        # skip if all nodes are Constant
        if all(self._is_constant_or_qdq(node) for node in nodes):
            return
        subonnx = graph.onnx_subgraph(nodes)
        out_nodes = {}
        constants = []
        for node_name in nx.topological_sort(subonnx):
            node_pb = subonnx.nodes[node_name]["pb"]
            if subonnx.nodes[node_name]["has_output"]:
                for out_name in node_pb.output:
                    if out_name in subonnx.outputs:
                        out_nodes[out_name] = node_pb
        # filter out the outputs that are exactly constant's output
        outputs_eval = set(subonnx.outputs)
        for node in list(filter(lambda n: n.op_type == "Constant", nodes)):
            if set(node.output).issubset(outputs_eval):
                nodes.remove(node)
                outputs_eval.difference_update(node.output)
        evaluator = Evaluator(subonnx.model)
        outputs = evaluator(outputs_eval, {})
        for output_name, out_value in zip(outputs_eval, outputs):
            constants.append(make_constant(output_name, out_value))
            constants[-1].output[0] = output_name  # keep the edge name
        self -= nodes
        self += constants


@L1.register(name="constantofshape_to_constant")
class ConstantOfShapeRewriter(Rewriter):
    """Rewrite ConstantOfShape to a constant node."""

    def __init__(self):
        super().__init__(pattern=SingleNodePattern("ConstantOfShape"))

    def rewrite(self, graph: OnnxGraph, nodes: List[NodeProto]):
        node = nodes[0]
        shape = self.get_value(node.input[0])  # from initializer
        if shape is None:
            # from constant node
            shape_node = self.get_input_node(node, 0)
            shape = self.get_value(shape_node)
            if shape is None:
                return
            self -= shape_node
        value = self.get_attribute(node, "value")
        if value is None:  # default value is 0.0
            value = np.array([0], dtype=np.float32)
        assert len(value) == 1
        value = value[0]
        const_node = make_constant(
            node.name + "/const", np.zeros(shape, dtype=value.dtype) + value
        )
        const_node.output[0] = node.output[0]
        self -= node
        self += const_node

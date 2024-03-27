"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import numpy as np
from onnx import TensorProto
from onnx.helper import (
    make_graph,
    make_model,
    make_node,
    make_operatorsetid,
    make_tensor,
    make_tensor_type_proto,
    make_value_info,
)

from onnx2onnx import OnnxGraph, PassManager
from onnx2onnx.evaluator import Evaluator


def _build_graph():
    # Create a graph with two inputs and one output
    # The first input is quantized with scale 0.5 and zero point 0
    # The second input is not quantized
    qnode0 = make_node(
        "QuantizeLinear",
        ["input0", "scale0", "zero_point0"],
        ["quantized0"],
        "quantize0",
    )
    dqnode0 = make_node(
        "DequantizeLinear",
        ["quantized0", "scale1", "zero_point1"],
        ["output0"],
        "dequantize0",
    )
    add = make_node("Add", ["output0", "input1"], ["sum"], "add")
    graph = make_graph(
        [qnode0, dqnode0, add],
        "graph",
        [
            make_value_info("input0", make_tensor_type_proto(1, [1, 3, 224, 224])),
            make_value_info("input1", make_tensor_type_proto(1, [1, 3, 224, 224])),
        ],
        [make_value_info("sum", make_tensor_type_proto(1, [1, 3, 224, 224]))],
        [
            make_tensor("scale0", 1, [], [1.0]),
            make_tensor("zero_point0", TensorProto.UINT8, [], [0]),
            make_tensor("scale1", 1, [], [1.0]),
            make_tensor("zero_point1", TensorProto.UINT8, [], [0]),
        ],
    )
    model = make_model(graph, opset_imports=[make_operatorsetid("", 19)])
    return model


def test_merge_quantize_input():
    graph = OnnxGraph(_build_graph())
    pm = PassManager(["initializer_to_constant", "infer_shape", "merge_quantize_input"])
    graph = pm.optimize(graph, strict=True)
    assert graph.tensor_type("input0") == TensorProto.UINT8
    assert graph.tensor_type("input1") == TensorProto.FLOAT

    ori_eval = Evaluator(_build_graph())
    opt_eval = Evaluator(graph.model)

    input0 = np.random.uniform(0, 255, size=[1, 3, 224, 224]).astype(np.float32)
    input1 = np.random.uniform(-128, 127, size=[1, 3, 224, 224]).astype(np.float32)
    qinput0 = np.round(input0).clip(0, 255).astype(np.uint8)
    ori_res = ori_eval(["sum"], {"input0": input0, "input1": input1})[0]
    opt_res = opt_eval(["sum"], {"input0": qinput0, "input1": input1})[0]
    assert np.allclose(ori_res, opt_res)

"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import onnx
from onnx.helper import make_graph, make_model, make_node, make_tensor_value_info

from onnx2onnx import OnnxGraph, PassManager


def _build_graph():
    node = make_node("Add", ["input1", "input2"], ["output1"])
    graph = make_graph(
        [node],
        "test_graph",
        [
            make_tensor_value_info("input1", onnx.TensorProto.FLOAT, [1, 2, 3]),
            make_tensor_value_info("input2", onnx.TensorProto.FLOAT, [1, 2, 3]),
            make_tensor_value_info("input3", onnx.TensorProto.FLOAT, [1, 2, 3]),
        ],
        [],
    )
    model = make_model(graph)
    onnx.checker.check_model(model)
    return model


def test_eliminate_unused_input():
    graph = OnnxGraph(_build_graph())
    pm = PassManager(["eliminate_unused_input"])
    graph = pm.optimize(graph, strict=True)
    assert len(graph.input) == 2
    assert len(graph.inputs) == 2

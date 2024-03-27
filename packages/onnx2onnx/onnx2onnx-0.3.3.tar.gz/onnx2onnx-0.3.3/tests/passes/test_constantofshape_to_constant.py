"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import numpy as np
import onnx
from onnx.helper import make_graph, make_model, make_node, make_tensor_value_info

from onnx2onnx import OnnxGraph, PassManager


def _build_graph():
    cos = make_node("ConstantOfShape", ["shape"], ["output"])
    graph = make_graph(
        [cos],
        "test_graph",
        [],
        [make_tensor_value_info("output", onnx.TensorProto.FLOAT, [2, 3])],
        initializer=[
            onnx.numpy_helper.from_array(np.array([2, 3], dtype=np.int64), "shape")
        ],
    )
    model = make_model(graph)
    onnx.checker.check_model(model, True)
    return model


def test_constantofshape_to_constant_from_initializer():
    model = _build_graph()
    graph = OnnxGraph(model)
    pm = PassManager(["constantofshape_to_constant"])
    graph = pm.optimize(graph, strict=True)
    assert len(graph.nodes) == 1
    for node in graph.nodes:
        node = graph.nodes[node]["pb"]
        assert node.op_type == "Constant"


def test_constantofshape_to_constant_from_constant():
    model = _build_graph()
    graph = OnnxGraph(model)
    pm = PassManager(["initializer_to_constant", "constantofshape_to_constant"])
    graph = pm.optimize(graph, strict=True)
    assert len(graph.nodes) == 1
    for node in graph.nodes:
        node = graph.nodes[node]["pb"]
        assert node.op_type == "Constant"

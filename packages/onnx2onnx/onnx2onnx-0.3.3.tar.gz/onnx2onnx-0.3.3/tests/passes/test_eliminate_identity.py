"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import numpy as np
from onnx import numpy_helper
from onnx.helper import (
    make_graph,
    make_model,
    make_node,
    make_operatorsetid,
    make_tensor_type_proto,
    make_value_info,
)

from onnx2onnx import PassManager
from onnx2onnx.graph import OnnxGraph


def _build_graph1():
    identity = make_node("Identity", ["x"], ["y"], "identity")
    relu = make_node("Relu", ["y"], ["z"], "relu")
    graph = make_graph(
        [identity, relu],
        "graph",
        [],
        [make_value_info("z", make_tensor_type_proto(1, [1, 3, 256, 256]))],
        [
            numpy_helper.from_array(
                np.random.randn(1, 3, 256, 256).astype(np.float32), "x"
            )
        ],
    )
    return make_model(graph, opset_imports=[make_operatorsetid("", 19)])


def _build_graph2():
    identity = make_node("Identity", ["x"], ["y"], "identity")
    relu1 = make_node("Relu", ["y"], ["z1"], "relu1")
    relu2 = make_node("Relu", ["y"], ["z2"], "relu2")
    relu3 = make_node("Relu", ["y"], ["z3"], "relu3")
    relu4 = make_node("Relu", ["y"], ["z4"], "relu4")
    graph = make_graph(
        [identity, relu1, relu2, relu3, relu4],
        "graph",
        [],
        [
            make_value_info("z1", make_tensor_type_proto(1, [1, 3, 256, 256])),
            make_value_info("z2", make_tensor_type_proto(1, [1, 3, 256, 256])),
            make_value_info("z3", make_tensor_type_proto(1, [1, 3, 256, 256])),
            make_value_info("z4", make_tensor_type_proto(1, [1, 3, 256, 256])),
        ],
        [
            numpy_helper.from_array(
                np.random.randn(1, 3, 256, 256).astype(np.float32), "x"
            )
        ],
    )
    return make_model(graph, opset_imports=[make_operatorsetid("", 19)])


def test_eliminate_identity_1fanout():
    model = _build_graph1()
    graph = OnnxGraph(model)
    pm = PassManager(["eliminate_identity"])
    graph = pm.optimize(graph, strict=True)
    assert len(graph.nodes) == 2
    assert "identity" not in graph


def test_eliminate_identity_4fanout():
    model = _build_graph2()
    graph = OnnxGraph(model)
    pm = PassManager(["eliminate_identity"])
    graph = pm.optimize(graph, strict=True)
    assert len(graph.nodes) == 8
    assert "identity" not in graph

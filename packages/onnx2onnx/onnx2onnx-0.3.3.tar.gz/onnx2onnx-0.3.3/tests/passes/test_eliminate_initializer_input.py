"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import numpy as np
import onnx
from onnx.helper import make_graph, make_node, make_tensor_value_info

from onnx2onnx import OnnxGraph, PassManager


def _build_graph():
    add = make_node("Add", ["x", "y"], ["z"])
    graph = make_graph(
        [add],
        "test",
        [
            make_tensor_value_info("x", onnx.TensorProto.FLOAT, [1, 1000]),
            make_tensor_value_info("y", onnx.TensorProto.FLOAT, [1, 1000]),
        ],
        [make_tensor_value_info("z", onnx.TensorProto.FLOAT, [1, 1000])],
        initializer=[
            onnx.numpy_helper.from_array(
                np.random.randn(1, 1000).astype(np.float32), "x"
            ),
            onnx.numpy_helper.from_array(
                np.random.randn(1, 1000).astype(np.float32), "y"
            ),
        ],
    )
    model = onnx.helper.make_model(graph)
    onnx.checker.check_model(model, full_check=True)
    return model


def test_eliminate_initializer_input():
    graph = OnnxGraph(_build_graph())
    pm = PassManager(["eliminate_initializer_input"])
    graph = pm.optimize(graph)
    assert len(graph.initializer) == 2
    assert len(graph.inputs) == 0

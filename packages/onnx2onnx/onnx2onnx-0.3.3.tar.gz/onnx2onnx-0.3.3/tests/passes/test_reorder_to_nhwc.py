"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import numpy as np
import onnx
from onnx.helper import (
    make_graph,
    make_model,
    make_node,
    make_operatorsetid,
    make_tensor_value_info,
)

from onnx2onnx import OnnxGraph, PassManager


def _build_graph_4d():
    conv = make_node("Convolution", ["x", "w", "b"], ["y"])
    graph = make_graph(
        [conv],
        "test",
        [
            make_tensor_value_info("x", onnx.TensorProto.FLOAT, [1, 3, 224, 224]),
            make_tensor_value_info("w", onnx.TensorProto.FLOAT, [64, 3, 7, 7]),
            make_tensor_value_info("b", onnx.TensorProto.FLOAT, [64]),
        ],
        [
            make_tensor_value_info("y", onnx.TensorProto.FLOAT, [1, 64, 218, 218]),
        ],
        [
            onnx.numpy_helper.from_array(
                np.random.randn(64, 3, 7, 7).astype(np.float32), "w"
            ),
            onnx.numpy_helper.from_array(np.random.randn(64).astype(np.float32), "b"),
        ],
    )
    model = make_model(graph, opset_imports=[make_operatorsetid("", 19)])
    return model


def _build_graph_5d():
    conv = make_node("Convolution", ["x", "w", "b"], ["y"])
    graph = make_graph(
        [conv],
        "test",
        [
            make_tensor_value_info("x", onnx.TensorProto.FLOAT, [1, 3, 16, 224, 224]),
            make_tensor_value_info("w", onnx.TensorProto.FLOAT, [64, 3, 3, 1, 1]),
            make_tensor_value_info("b", onnx.TensorProto.FLOAT, [64]),
        ],
        [
            make_tensor_value_info("y", onnx.TensorProto.FLOAT, [1, 64, 14, 224, 224]),
        ],
        [
            onnx.numpy_helper.from_array(
                np.random.randn(64, 3, 3, 1, 1).astype(np.float32), "w"
            ),
            onnx.numpy_helper.from_array(np.random.randn(64).astype(np.float32), "b"),
        ],
    )
    model = make_model(graph, opset_imports=[make_operatorsetid("", 19)])
    return model


def test_reorder_to_nhwc():
    graph = OnnxGraph(_build_graph_4d())
    pm = PassManager(["reorder_to_nhwc"])
    graph = pm.optimize(graph, strict=True)
    assert graph.tensor_shape("x_nhwc") == [1, 224, 224, 3]


def test_reorder_to_nhwc_failure_case():
    graph = OnnxGraph(_build_graph_5d())
    pm = PassManager(["reorder_to_nhwc"])
    graph = pm.optimize(graph, strict=True)
    assert graph.tensor_shape("x_nhwc") is None
    assert graph.tensor_shape("x") == [1, 3, 16, 224, 224]

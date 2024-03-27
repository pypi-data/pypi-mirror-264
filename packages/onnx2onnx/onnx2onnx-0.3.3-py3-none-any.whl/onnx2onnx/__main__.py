"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

# pylint: disable=missing-function-docstring

import argparse
import json
from pathlib import Path

from . import PassManager, convert_graph

USAGE = "onnx2onnx input_model.onnx [output_model.onnx]"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="onnx2onnx",
        usage=USAGE,
        description="onnx2onnx command-line api",
    )
    parser.add_argument(
        "-a",
        "--activate",
        nargs="*",
        help="select passes to be activated, activate all passes if not set.",
    )
    parser.add_argument(
        "--l1",
        nargs="*",
        help="append specified passes after l1 passes.",
    )
    parser.add_argument(
        "--l2",
        nargs="*",
        help="append specified passes after l2 passes.",
    )
    parser.add_argument(
        "--print-all",
        action="store_true",
        help="print the name of all optimizing passes",
    )
    parser.add_argument(
        "--print-l1",
        action="store_true",
        help="print the name of level 1 optimizing passes",
    )
    parser.add_argument(
        "--print-l2",
        action="store_true",
        help="print the name of level 2 optimizing passes",
    )
    parser.add_argument(
        "--format",
        choices=("protobuf", "textproto", "json", "onnxtxt"),
        default=None,
        help="onnx file format",
    )
    parser.add_argument(
        "-s", "--infer-shapes", action="store_true", help="infer model shapes"
    )
    parser.add_argument(
        "-c", "--config-file", help="specify a json-format config file for passes"
    )

    return parser.parse_known_args()


def main():
    args, argv = parse_args()

    if args.print_all:
        PassManager.print_all()
        exit(0)
    elif args.print_l1:
        PassManager.print_l1()
        exit(0)
    elif args.print_l2:
        PassManager.print_l2()
        exit(0)
    if len(argv) == 1:
        input_model = Path(argv[0])
        output_model = Path(input_model.stem + "_o2o")
    elif len(argv) == 2:
        input_model = Path(argv[0])
        output_model = Path(argv[1])
    else:
        print("Usage: " + USAGE)
        if len(argv) == 0:
            raise RuntimeError("missing input model")
        else:
            raise RuntimeError("unknown argument: " + ",".join(argv[2:]))

    if args.config_file:
        with open(args.config_file, encoding="utf-8") as file:
            configs = json.load(file)
    else:
        configs = None

    graph = convert_graph(input_model, args.activate, args.format, configs=configs)
    graph.save(output_model, format=args.format, infer_shapes=args.infer_shapes)
    print(f"model saved to {output_model}")


if __name__ == "__main__":
    main()

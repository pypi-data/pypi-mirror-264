"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import inspect
from typing import Callable, Iterator, List, Optional

from tabulate import tabulate


class Registry:
    """A simple registry object to hold objects from others

    Samples::

        FOO = Registry("FOO")

        @FOO.register()
        def foo(): ...

        print(FOO)
        # ┌───────────────┐
        # │ Register: FOO │
        # ├───────────────┤
        # │ foo           │
        # └───────────────┘
    """

    def __init__(self, name=None, parent: "Registry" = None) -> None:
        self._bucks = {}
        self._configs = {}
        self._name = name or "<Registry>"
        self._parent = parent
        if parent is not None:
            self._name = f"{parent.name}.{self.name}"

    @property
    def name(self) -> str:
        """Return the name of the registry."""
        return self._name

    @staticmethod
    def _legal_name(name: str) -> str:
        words = [""]
        for a, b in zip(list(name), list(name.lower())):
            if a != b:
                words.append("")
            words[-1] += b
        return "_".join(words).strip("_")

    def register(self, name=None, deps: List[str] = None):
        """A decorator to register an object."""

        def wrapper(func):
            if not callable(func):
                raise TypeError(
                    "the object to be registered must be a function or Rewriter,"
                    f" got {type(func)}"
                )
            # set default dependency list to empty
            setattr(func, "__deps__", deps or [])
            if inspect.isfunction(func):
                func.__name__ = name or func.__name__
                self._bucks[func.__name__] = func
                self._configs[func.__name__] = inspect.signature(func)
            else:
                obj = func()
                if not (hasattr(obj, "rewrite") and inspect.ismethod(obj.rewrite)):
                    raise TypeError(
                        f"the registered object {func} must be the subclass "
                        "of onnx2onnx.passes.rewriter.Rewriter, but its mro is "
                        f"{func.__mro__}"
                    )
                assert callable(obj), f"Wired! {func} is not callable!"

                obj.__name__ = name or self._legal_name(func.__name__)
                self._bucks[obj.__name__] = obj
                self._configs[obj.__name__] = inspect.signature(func.rewrite)
            if self._parent is not None:
                self._parent.register(name, deps)(func)
            return func

        return wrapper

    def get(self, name: str) -> Optional[Callable]:
        """Get a registered object by its name."""
        return self._bucks.get(name)

    def get_config(self, name: str):
        """Get the configuration of an object"""
        return self._configs.get(name)

    def __iter__(self) -> Iterator[Callable]:
        """Return an Iterator for all registered functions"""
        yield from self._bucks.keys()

    def __contains__(self, name: str) -> bool:
        """Check if a function is registered"""
        return name in self._bucks

    def __repr__(self) -> str:
        title = [f"Register: {self._name}", "Args", "Deps"]
        members = []
        for i in sorted(self._bucks.keys()):
            members.append([i, self._configs[i], self._bucks[i].__deps__])
        return tabulate(members, title, "simple_grid")


PASSES = Registry("PASS")
L1 = Registry("L1", parent=PASSES)
L2 = Registry("L2", parent=PASSES)
L3 = Registry("L3", parent=PASSES)

# pylint: disable=C0413
from .convert import *  # noqa: E402, F403
from .optimize import *  # noqa: E402, F403
from .quantize import *  # noqa: E402, F403
from .transforms import *  # noqa: E402, F403

# pylint: enable=C0413

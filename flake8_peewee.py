import sys
import ast

from typing import Any
from typing import Generator
from typing import List
from typing import Tuple
from typing import Type

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

PWE101 = "PWE101 select() or delete() inner comparison expression are not allowed"


def _get_pwe101(node: ast.Call):
    errors: List[Tuple[int, int, str]] = []
    if (
            isinstance(node.func, ast.Attribute) and
            node.func.attr in ("select", "delete") and
            len(node.args) > 0 and
            isinstance((node.args[0]), ast.Compare)

    ):
        errors.append(
            (node.lineno, node.col_offset, PWE101)
        )

    return errors


class Visitor(ast.NodeVisitor):

    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call):
        self.errors += _get_pwe101(node)
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)

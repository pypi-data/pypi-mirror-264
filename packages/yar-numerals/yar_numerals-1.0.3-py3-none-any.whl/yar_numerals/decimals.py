from .grammar import *
from .syntax import *
from . import fractionals


def inflect(
    whole: str,
    decimal: str,
    form: InflectionForm,
    insert_ones=False,
    strict_range=False,
) -> str:
    magnitude = get_decimal_fraction_magnitude(decimal)

    root = DummySyntaxNode(form)
    obj = DummySyntaxNode({})

    fractionals.build_tree(
        root, obj, whole, decimal, magnitude, insert_ones, strict_range
    )
    root.agree()
    return str(root)


def get_decimal_fraction_magnitude(decimal: str) -> str:
    return "1" + "0" * len(decimal)

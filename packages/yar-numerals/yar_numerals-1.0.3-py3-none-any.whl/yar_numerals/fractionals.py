from .grammar import *
from .syntax import *
from . import cardinals, ordinals
from .lexeme import NumeralLexeme


def inflect(
    whole: str,
    numerator: str,
    denominator: str,
    form: InflectionForm,
    insert_ones=False,
    strict_range=False,
) -> str:
    root = DummySyntaxNode(form)
    obj = DummySyntaxNode({})

    build_tree(root, obj, whole, numerator, denominator, insert_ones, strict_range)
    root.agree()
    return str(root)


def build_tree(
    root: SyntaxNode,
    obj: SyntaxNode,
    whole: str,
    numerator: str,
    denominator: str,
    insert_ones=False,
    strict_range=False,
) -> None:
    # Add a dummy node for the virtual lexeme "частина" as in
    #  1/4 = одна четверта [частина]
    vroot_part = DummySyntaxNode(
        persistent_form=InflectionForm(gender="feminine", animacy="inanimate"),
    )
    root.add_child_node(vroot_part, Relation.amod)
    vroot_part.add_child_node(obj, Relation.nmod)
    ordinals.build_tree(vroot_part, denominator, insert_ones, strict_range)
    cardinals.build_tree(vroot_part, numerator, insert_ones, strict_range)
    _fix_puacal(vroot_part)

    if whole:
        # Add a dummy node for the virtual lexeme "частина" as in
        #  1 1/4 = одна ціла [частина] одна четверта
        vroot_whole_parts = DummySyntaxNode(
            persistent_form=InflectionForm(gender="feminine", animacy="inanimate"),
        )
        root.add_child_node(vroot_whole_parts, Relation.amod)
        whole_adj = vroot_whole_parts.add_child(
            NumeralLexeme.misc("whole"), Relation.amod
        )
        cardinals.build_tree(vroot_whole_parts, whole, insert_ones, strict_range)
        _fix_puacal(vroot_whole_parts)


def _fix_puacal(root: SyntaxNode):
    for edge in root.edges:
        if edge.rel == Relation.nummod_govpc:
            edge.rel = Relation.nummod_govpl

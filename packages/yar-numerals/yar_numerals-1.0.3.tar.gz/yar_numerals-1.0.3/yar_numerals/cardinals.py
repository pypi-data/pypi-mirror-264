from typing import List
from .grammar import *
from .lexeme import *
from .syntax import *
from . import errors

MAX_DIGIT_COUNT = 27


def inflect(
    whole: str,
    form: InflectionForm,
    insert_ones: bool = False,
    strict_range: bool = False,
) -> str:
    """
    Produce an inflected spelling of the provided whole cardinal number.

    *Note:* Input values are not validated, the recommended API is :any:`inflect_cardinal`

    :param whole: The sequence of base 10 digits to be spelled out.
    :param form: The grammatical form of the generated text.
    :param insert_ones: Whether the output should insert "ones" in thousands and millions.
    :param strict_range: Whether to throw an exception when the number is too big to correctly process.
    :return: The spellout of the provided whole cardinal number in a given form.
    """
    root = DummySyntaxNode(form)
    build_tree(root, whole, insert_ones, strict_range)
    root.agree()
    return str(root)


def build_tree(
    root: SyntaxNode, number: str, insert_ones: bool = False, strict_range: bool = False
) -> None:
    number = number.lstrip("0")
    if len(number) == 0:
        root.add_child(NumeralLexeme.cardinal("0"), Relation.nummod_govpl)
        return
    digits = list(number)
    build_tree_from_digits(root, digits, insert_ones, strict_range)


def build_tree_from_digits(
    root: SyntaxNode, digits: List[str], insert_ones: bool, strict_range: bool
) -> None:
    if len(digits) > MAX_DIGIT_COUNT:
        if strict_range:
            raise errors.RangeError(digits, MAX_DIGIT_COUNT)
        else:
            return build_tree_digit_wise(root, digits)

    is_first = True
    power = 0

    while len(digits) > 0:
        if len(digits) < 3:
            [*digits, hundreds, tens, ones] = ["0", "0", *digits]
        else:
            [*digits, hundreds, tens, ones] = digits
        lexemes = list(triplet_into_lexemes(hundreds, tens, ones))
        if len(lexemes) > 0:
            current_root = root
            if power > 0:
                countable_lexeme = NumeralLexeme.cardinal("1" + "0" * power)
                current_root = root.add_child(
                    countable_lexeme, get_relation_type(countable_lexeme, is_first)
                )
                is_first = True

            if not insert_ones and power > 0:
                if len(lexemes) == 1 and lexemes[0].value == "1":
                    continue
            for lexeme in lexemes:
                current_root.add_child(lexeme, get_relation_type(lexeme, is_first))
                is_first = False
        power += 3


def build_tree_digit_wise(root, digits):
    [*remaining_parts, inflected_part] = digits
    root.add_child(NumeralLexeme.cardinal(inflected_part), Relation.nummod)
    for digit in remaining_parts[::-1]:
        root.add_child(NumeralLexeme.cardinal(digit), Relation.num)
    return


def get_relation_type(lexeme, is_first):
    if not is_first:
        return Relation.nummod
    if lexeme.value == "1":
        return Relation.nummod_govsg
    if lexeme.value in ("2", "3", "4"):
        return Relation.nummod_govpc
    else:
        return Relation.nummod_govpl


def triplet_into_lexemes(hundreds, tens, ones):
    if tens == "1":
        yield NumeralLexeme.cardinal(tens + ones)
    else:
        if ones != "0":
            yield NumeralLexeme.cardinal(ones)
        if tens != "0":
            yield NumeralLexeme.cardinal(tens + "0")
    if hundreds != "0":
        yield NumeralLexeme.cardinal(hundreds + "00")

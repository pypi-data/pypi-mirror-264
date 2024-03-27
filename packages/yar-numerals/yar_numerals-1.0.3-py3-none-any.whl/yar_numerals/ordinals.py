from typing import List
from .grammar import *
from .lexeme import *
from .syntax import *
from . import cardinals, errors

MAX_DIGIT_COUNT = 27


def inflect(
    whole: str, form: InflectionForm, insert_ones=False, strict_range=False
) -> str:
    root = DummySyntaxNode(form)
    build_tree(root, whole, insert_ones, strict_range)
    root.agree()
    return str(root)


def build_tree(
    root: SyntaxNode, number: str, insert_ones: bool = False, strict_range: bool = False
) -> None:
    number = number.lstrip("0")
    if len(number) == 0:
        root.add_child(NumeralLexeme.ordinal("0"), Relation.nummod)
        return
    digits = list(number)
    build_tree_from_digits(root, digits, insert_ones, strict_range)


def build_tree_from_digits(
    root: SyntaxNode, digits: List[str], insert_ones: bool, strict_range: bool
):
    if len(digits) > MAX_DIGIT_COUNT:
        if strict_range:
            raise errors.RangeError(digits, MAX_DIGIT_COUNT)
        else:
            return build_tree_digit_wise(root, digits)

    power = 0
    while len(digits) > 0:
        if len(digits) < 3:
            [*digits, hundreds, tens, ones] = ["0", "0", *digits]
        else:
            [*digits, hundreds, tens, ones] = digits
        numbers = list(triplet_into_monolexemic_numbers(hundreds, tens, ones))

        if len(numbers) > 0:
            if power == 0:
                [ord, *card] = numbers
                root.add_child(NumeralLexeme.ordinal(ord), Relation.amod)

                for n in card:
                    root.add_child(NumeralLexeme.cardinal(n), Relation.num)
                break
            else:
                large_number = "1" + "0" * power
                if numbers == ["1"]:
                    root.add_child(
                        NumeralLexeme.ordinal(large_number),
                        Relation.amod,
                    )
                else:
                    compound_lexeme = NumeralLexeme.ordinal_compound(
                        numbers, large_number
                    )
                    root.add_child(compound_lexeme, Relation.nummod)
                break

        power += 3
    power += 3

    # The remaining parts should be inflected as a cardinal
    is_first = False
    while len(digits) > 0:
        if len(digits) < 3:
            [*digits, hundreds, tens, ones] = ["0", "0", *digits]
        else:
            [*digits, hundreds, tens, ones] = digits
        lexemes = list(cardinals.triplet_into_lexemes(hundreds, tens, ones))
        if len(lexemes) > 0:
            countable_lexeme = NumeralLexeme.cardinal("1" + "0" * power)
            current_root = root.add_child(countable_lexeme, Relation.num)
            is_first = True

            if not insert_ones:
                if len(lexemes) == 1 and lexemes[0].value == "1":
                    continue
            for lexeme in lexemes:
                current_root.add_child(
                    lexeme, cardinals.get_relation_type(lexeme, is_first)
                )
                is_first = False
        power += 3


def build_tree_digit_wise(root: SyntaxNode, digits: List[str]) -> None:
    [*cardinal_parts, ordinal_part] = digits
    root.add_child(NumeralLexeme.ordinal(ordinal_part), Relation.nummod)
    for digit in cardinal_parts[::-1]:
        root.add_child(NumeralLexeme.cardinal(digit), Relation.num)


def triplet_into_monolexemic_numbers(hundreds, tens, ones):
    if tens == "1":
        yield tens + ones
    else:
        if ones != "0":
            yield ones
        if tens != "0":
            yield tens + "0"
    if hundreds != "0":
        yield hundreds + "00"

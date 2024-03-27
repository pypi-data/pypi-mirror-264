# (c) Copyright by Yar.
#
# The basic API definitions for the numerals module.

from . import (
    cardinals,
    decimals,
    fractionals,
    grammar,
    errors,
    grapheme,
    ordinals,
    validator,
)

__all__ = [
    "inflect_cardinal",
    "inflect_ordinal",
    "inflect_decimal",
    "inflect_fractional",
    "grammar",
    "errors",
]


def inflect_cardinal(
    whole: str,
    form: grammar.InflectionForm,
    stress: bool = False,
    insert_ones: bool = False,
    strict_range: bool = False,
) -> str:
    """
    Returns a spelling of the provided non-negative integer number as a cardinal
    numeral. The spelling is inflected for a requested form. The input is validated and
    exception of type descending from :any:`errors.YarNumBaseError` is thrown if
    validation fails. The range of numbers that can be correctly inflected is [0...1e27);
    numbers outside this range are not processed correctly. See `strict_range` for more
    details.

    :param whole: The string of digits in base 10 to be spelled out.
    :param form: The grammatical form of the generated text.
    :param stress: Whether the output text should contain stresses.
    :param insert_ones: Whether the output should insert "ones" in thousands and millions.
    :param strict_range: Whether to throw an exception when the number is too big to
    correctly process.
    :return: The spellout of the provided number as a cardinal numeral inflected for a given form.

    Basic usage
        >>> inflect_cardinal("43", {"case": "nominative"})
        'сорок три'
        >>> inflect_cardinal("43", {"case": "genitive"})
        'сорока трьох'

    Using `stress` parameter
        >>> inflect_cardinal("75", {}, stress=False)
        'сімдесят пʼять'
        >>> inflect_cardinal("75", {}, stress=True)
        'сімдеся́т пʼя́ть'

    Using `insert_ones` parameter
        >>> inflect_cardinal("1000", {}, insert_ones=False)
        'тисяча'
        >>> inflect_cardinal("1000", {}, insert_ones=True)
        'одна тисяча'

    Using `strict_range` parameter
        >>> inflect_cardinal("100000000000000000000000000", {}, strict_range=False)
        'сто септильйонів'
        >>> inflect_cardinal("1000000000000000000000000000", {}, strict_range=False)
        'один нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль'
        >>> inflect_cardinal("1000000000000000000000000000", {}, strict_range=True)
        Traceback (most recent call last):
            ...
        yar_numerals.errors.RangeError: Provided number is too large with 28 out of 27 digits.
    """
    validator.validate_int(whole)
    validator.validate_form(form)
    text = cardinals.inflect(whole, form, insert_ones, strict_range)
    if not stress:
        text = grapheme.remove_stress(text)
    return text


def inflect_ordinal(
    whole: str,
    form: grammar.InflectionForm,
    stress: bool = False,
    insert_ones: bool = False,
    strict_range: bool = False,
) -> str:
    """
    Returns a spelling of the provided non-negative integer number as an ordinal
    numeral. The spelling is inflected for a requested form. The input is validated and
    exception of type descending from :any:`errors.YarNumBaseError` is thrown if
    validation fails. The range of numbers that can be correctly inflected is [0...1e27);
    numbers outside this range are not processed correctly. See `strict_range` for more
    details.

    :param whole: The string of digits in base 10 to be spelled out.
    :param form: The grammatical form of the generated text.
    :param stress: Whether the output text should contain stresses.
    :param insert_ones: Whether the output should insert "ones" in thousands and millions.
    :param strict_range: Whether to throw an exception when the number is too big to
    correctly process.
    :return: The spellout of the provided number as a ordinal numeral inflected for a given form.

    Basic usage
        >>> inflect_ordinal("43", {"case": "nominative"})
        'сорок третій'
        >>> inflect_ordinal("43", {"case": "genitive", "gender": "feminine"})
        'сорок третьої'

    Using `stress` parameter
        >>> inflect_ordinal("75", {}, stress=False)
        'сімдесят пʼятий'
        >>> inflect_ordinal("75", {}, stress=True)
        'сімдеся́т пʼя́тий'

    Using `insert_ones` parameter
        >>> inflect_ordinal("1001", {}, insert_ones=False)
        'тисяча перший'
        >>> inflect_ordinal("1001", {}, insert_ones=True)
        'одна тисяча перший'

    Using `strict_range` parameter
        >>> inflect_ordinal("100000000000000000000000000", {}, strict_range=False)
        'стасептильйонний'
        >>> inflect_ordinal("1000000000000000000000000000", {}, strict_range=False)
        'один нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нульовий'
        >>> inflect_ordinal("1000000000000000000000000000", {}, strict_range=True)
        Traceback (most recent call last):
            ...
        yar_numerals.errors.RangeError: Provided number is too large with 28 out of 27 digits.
    """
    validator.validate_int(whole)
    validator.validate_form(form)
    text = ordinals.inflect(whole, form, insert_ones, strict_range)
    if not stress:
        text = grapheme.remove_stress(text)
    return text


def inflect_decimal(
    whole: str,
    fractional: str,
    form: grammar.InflectionForm,
    stress: bool = False,
    insert_ones: bool = False,
    strict_range: bool = False,
) -> str:
    """
    Returns a spelling of the provided decimal fractional number as a cardinal
    numeral. The spelling is inflected for a requested form. The input is validated and
    exception of type descending from :any:`errors.YarNumBaseError` is thrown if
    validation fails. The number that can be correctly spelled only if every component
    of the fraction is in range [0...1e27); numbers with components outside of this
    range are not processed correctly. See `strict_range` for more details.

    :param whole: The string of digits in base 10 to be spelled out.
    :param fractional: The string of digits in base 10 to be spelled out.
    :param form: The grammatical form of the generated text.
    :param stress: Whether the output text should contain stresses.
    :param insert_ones: Whether the output should insert "ones" in thousands and millions.
    :param strict_range: Whether to throw an exception when the number is too big to
    correctly process.
    :return: The spellout of the provided number as a cardinal numeral inflected for a given form.

    Basic usage
        >>> inflect_cardinal("43", {"case": "nominative"})
        'сорок три'
        >>> inflect_cardinal("43", {"case": "genitive"})
        'сорока трьох'

    Using `stress` parameter
        >>> inflect_cardinal("75", {}, stress=False)
        'сімдесят пʼять'
        >>> inflect_cardinal("75", {}, stress=True)
        'сімдеся́т пʼя́ть'

    Using `insert_ones` parameter
        >>> inflect_cardinal("1000", {}, insert_ones=False)
        'тисяча'
        >>> inflect_cardinal("1000", {}, insert_ones=True)
        'одна тисяча'

    Using `strict_range` parameter
        >>> inflect_cardinal("100000000000000000000000000", {}, strict_range=False)
        'сто септильйонів'
        >>> inflect_cardinal("1000000000000000000000000000", {}, strict_range=False)
        'один нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль нуль'
        >>> inflect_cardinal("1000000000000000000000000000", {}, strict_range=True)
        Traceback (most recent call last):
            ...
        yar_numerals.errors.RangeError: Provided number is too large with 28 out of 27 digits.
    """
    validator.validate_int(whole)
    validator.validate_int(fractional)
    validator.validate_form(form)
    text = decimals.inflect(whole, fractional, form, insert_ones, strict_range)
    if not stress:
        text = grapheme.remove_stress(text)
    return text


def inflect_fractional(
    whole: str,
    numerator: str,
    denominator: str,
    form: grammar.InflectionForm,
    stress=False,
    insert_ones=False,
    strict_range=False,
) -> str:
    """
    Returns a spelling of the provided fractional number as a cardinal numeral.
    The spelling is inflected for a requested form. The input is validated and
    exception of type descending from :any:`errors.YarNumBaseError` is thrown if
    validation fails. The number that can be correctly spelled only if every component
    of the fraction is in range [0...1e27); numbers with components outside of this
    range are not processed correctly. See `strict_range` for more details.
    """
    validator.validate_int(whole)
    validator.validate_int(numerator)
    validator.validate_int(denominator)
    validator.validate_form(form)
    text = fractionals.inflect(
        whole, numerator, denominator, form, insert_ones, strict_range
    )
    if not stress:
        text = grapheme.remove_stress(text)
    return text

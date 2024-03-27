from typing import Tuple
from . import *
from .grammar import *
from .errors import *
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import argparse, sys

parser = argparse.ArgumentParser(
    prog="Yar.Numerals",
    description="""Inflector for Ukrainian numerals.
    \nConverts digits into spoken word in desired form.""",
    epilog="Deliverd by the Yar team.",
)

parser.add_argument("value", help="the number to inflect")


case_group = parser.add_mutually_exclusive_group()
case_group.add_argument(
    "-c",
    "--case",
    type=Case,
    choices=list(Case),
    help="set grammatical case to inflect to",
    default=Case.nominative,
)
simple_case_group = case_group.add_mutually_exclusive_group()
simple_case_group.add_argument(
    "--nom",
    action="store_const",
    dest="case",
    const=Case.nominative,
    help="inflect to nominative case, DEFAULT",
)
simple_case_group.add_argument(
    "--gen",
    action="store_const",
    dest="case",
    const=Case.genitive,
    help="inflect to genitive case",
)
simple_case_group.add_argument(
    "--dat",
    action="store_const",
    dest="case",
    const=Case.dative,
    help="inflect to dative case",
)
simple_case_group.add_argument(
    "--acc",
    action="store_const",
    dest="case",
    const=Case.accusative,
    help="inflect to accusative case",
)
simple_case_group.add_argument(
    "--inst",
    action="store_const",
    dest="case",
    const=Case.instrumental,
    help="inflect to instrumental case",
)
simple_case_group.add_argument(
    "--loc",
    action="store_const",
    dest="case",
    const=Case.locative,
    help="inflect to locative case",
)
simple_case_group.add_argument(
    "--voc",
    action="store_const",
    dest="case",
    const=Case.vocative,
    help="inflect to vocative case",
)

gender_group = parser.add_mutually_exclusive_group()
gender_group.add_argument(
    "-g",
    "--gender",
    type=Gender,
    choices=list(Gender),
    help="set grammatical gender to inflect to",
    default=Gender.masculine,
)
simple_gender_group = gender_group.add_mutually_exclusive_group()
simple_gender_group.add_argument(
    "--m",
    action="store_const",
    dest="gender",
    const=Gender.masculine,
    help="inflect to masculine grammatical gender, DEFAULT",
)
simple_gender_group.add_argument(
    "--f",
    action="store_const",
    dest="gender",
    const=Gender.feminine,
    help="inflect to feminine grammatical gender",
)
simple_gender_group.add_argument(
    "--n",
    action="store_const",
    dest="gender",
    const=Gender.neuter,
    help="inflect to neuter grammatical gender",
)

number_group = parser.add_mutually_exclusive_group()
number_group.add_argument(
    "-n",
    "--number",
    type=Number,
    choices=list(Number),
    help="set grammatical number to inflect to",
    default=Number.singular,
)
simple_number_group = number_group.add_mutually_exclusive_group()
simple_number_group.add_argument(
    "--sg",
    action="store_const",
    dest="number",
    const=Number.singular,
    help="inflect to singular number, DEFAULT",
)
simple_number_group.add_argument(
    "--pl",
    action="store_const",
    dest="number",
    const=Number.plural,
    help="inflect to plural number",
)

animacy_group = parser.add_mutually_exclusive_group()
animacy_group.add_argument(
    "-a",
    "--animacy",
    type=Animacy,
    choices=list(Animacy),
    help="set grammatical animacy",
)
simple_animacy_group = animacy_group.add_mutually_exclusive_group()
simple_animacy_group.add_argument(
    "--inan",
    action="store_const",
    dest="animacy",
    const=Animacy.inanimate,
    help="inflect to plural number, DEFAULT",
)
simple_animacy_group.add_argument(
    "--anim",
    action="store_const",
    dest="animacy",
    const=Animacy.animate,
    help="inflect to singular number",
)

type_group = parser.add_mutually_exclusive_group()
type_group.add_argument(
    "--cardinal", action="store_true", help="inflect into cardinal form, DEFAULT"
)
type_group.add_argument(
    "--ordinal",
    action="store_true",
    help="inflect into ordinal form, NOTE: only for integers",
)
type_group.add_argument(
    "--decimal", action="store_true", help="inflect as decimal fraction"
)

parser.add_argument("--stress", action="store_true", help="result will include stress")

args = parser.parse_args()


def parse_float(v: str) -> Tuple[str, str]:
    try:
        _ = float(v)
    except ValueError:
        raise errors.YarNumBaseError(
            f"Provided value is not a valid decimal fraction: {str(v)}"
        ) from None
    import re

    parts = re.split(
        r",|\.", v
    )  # Ukrainian locale uses comma as a decimal separator but this is not guaranteed to be true for input
    if len(parts) <= 2:
        whole, fractional, *_ = *parts, ""
        return whole, fractional
    else:
        raise errors.YarNumBaseError(
            f"Provided value is not a valid decimal fraction {str(v)}"
        )


def inflect(args: argparse.Namespace) -> str:
    form = InflectionForm(**vars(args))
    if args.ordinal:
        return inflect_ordinal(args.value, form, stress=args.stress)
    if args.decimal:
        whole, fractional = parse_float(args.value)
        print(whole, fractional)
        return inflect_decimal(whole, fractional, form, stress=args.stress)
    try:
        return inflect_cardinal(args.value, form, stress=args.stress)
    except NonIntegerInputError:
        pass
    whole, fractional = parse_float(args.value)
    return inflect_decimal(whole, fractional, form, stress=args.stress)


try:
    result = inflect(args)
    print(result)
    sys.exit(0)
except YarNumBaseError as e:
    print("Error:", str(e), file=sys.stderr)
    sys.exit(1)

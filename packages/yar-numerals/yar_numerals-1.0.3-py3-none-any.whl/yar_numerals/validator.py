import re

from .errors import *
from .grammar import *

_intRegex = re.compile(r"\s*\d+\s*")


def validate_int(v: str):
    if not _intRegex.fullmatch(v):
        raise NonIntegerInputError(v)


def validate_form(f: InflectionForm):
    case = f.get("case")
    if case:
        if case not in list(Case):
            raise InvalidFormError(f"case has invalid value: {str(case)}")
    gender = f.get("gender")
    if gender:
        if gender not in list(Gender):
            raise InvalidFormError(f"gender has invalid value: {str(gender)}")
    number = f.get("number")
    if number:
        if number not in list(Number):
            raise InvalidFormError(f"number has invalid value: {str(number)}")
    animacy = f.get("animacy")
    if animacy:
        if animacy not in list(Animacy):
            raise InvalidFormError(f"animacy has invalid value: {str(animacy)}")

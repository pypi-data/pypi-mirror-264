from enum import Enum
from typing import TypedDict, Optional

__all__ = [
    "Case",
    "Gender",
    "Number",
    "Animacy",
    "InflectionForm",
    "default_inflection_form",
]


class _StrEnum(str, Enum):
    def __str__(self):  # pragma: no cover
        return self.value


class Case(_StrEnum):
    nominative = "nominative"
    genitive = "genitive"
    dative = "dative"
    accusative = "accusative"
    instrumental = "instrumental"
    locative = "locative"
    vocative = "vocative"


class Gender(_StrEnum):
    masculine = "masculine"
    feminine = "feminine"
    neuter = "neuter"
    common = "common"


class Number(_StrEnum):
    singular = "singular"
    plural = "plural"


class Animacy(_StrEnum):
    inanimate = "inanimate"
    animate = "animate"


class InflectionForm(TypedDict):
    case: Optional["Case"]
    gender: Optional["Gender"]
    number: Optional["Number"]
    animacy: Optional["Animacy"]


def default_inflection_form():
    return InflectionForm(
        case=Case.nominative,
        gender=Gender.masculine,
        number=Number.singular,
        animacy=Animacy.inanimate,
    )

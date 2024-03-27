# (c) Copyright by Yar.
#
# Syntactic relation types and agreement logic.

from typing import Optional
from enum import Enum
from ..lexeme import Lexeme
from ..grammar import *

__all__ = ["Relation", "RelationDef"]


class _StrEnum(str, Enum):
    def __str__(self):  # pragma: no cover
        return self.value


class Relation(_StrEnum):
    nmod = "nmod"
    amod = "amod"
    num = "num"
    nummod = "nummod"
    nummod_govsg = "nummod:govsg"
    nummod_govpc = "nummod:govpc"
    nummod_govpl = "nummod:govpl"


class RelationDef:
    @staticmethod
    def modifier(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        return None

    @staticmethod
    def governing(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        return None

    @staticmethod
    def get(name: Relation) -> type["RelationDef"]:
        return {
            Relation.nmod: RelationDef_NMod,
            Relation.amod: RelationDef_AMod,
            Relation.num: RelationDef_Num,
            Relation.nummod: RelationDef_NumMod,
            Relation.nummod_govsg: RelationDef_NumMod_GovSg,
            Relation.nummod_govpc: RelationDef_NumMod_GovPc,
            Relation.nummod_govpl: RelationDef_NumMod_GovPl,
        }[name]


class RelationDef_Num(RelationDef):
    pass


class RelationDef_AMod(RelationDef):
    @staticmethod
    def modifier(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        return InflectionForm(
            case=src.form.get("case"),
            gender=src.form.get("gender"),
            animacy=src.form.get("animacy"),
            number=src.form.get("number"),
        )


class RelationDef_NMod(RelationDef):
    @staticmethod
    def modifier(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        return InflectionForm(
            case=Case.genitive,
            gender=src.form.get("gender"),
            animacy=src.form.get("animacy"),
            number=src.form.get("number"),
        )


class RelationDef_NumMod(RelationDef):
    @staticmethod
    def modifier(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        return InflectionForm(
            case=src.form.get("case"),
            gender=src.form.get("gender"),
            animacy=src.form.get("animacy"),
            number=src.form.get("number"),
        )


class RelationDef_NumMod_GovSg(RelationDef_NumMod):
    @staticmethod
    def governing(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        return InflectionForm(number=Number.singular)


class RelationDef_NumMod_GovPc(RelationDef_NumMod):
    @staticmethod
    def governing(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        return InflectionForm(number=Number.plural)


class RelationDef_NumMod_GovPl(RelationDef_NumMod):
    @staticmethod
    def governing(src: Lexeme, dst: Lexeme) -> Optional[InflectionForm]:
        form = InflectionForm(number=Number.plural)
        if dst.form.get("case") in [Case.nominative, Case.accusative]:
            form.update(case=Case.genitive)
        return form

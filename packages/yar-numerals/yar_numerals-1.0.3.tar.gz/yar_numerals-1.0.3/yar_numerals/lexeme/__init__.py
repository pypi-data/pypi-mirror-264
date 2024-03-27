# (c) Copyright by Yar.
#
# Lexical layer of processing.

from typing import List, Tuple
from ..errors import InternalDataError
from ..grammar import *
from .numeral import cardinal, cardinal_stem, ordinal, misc

__all__ = [
    "Lexeme",
    "DummyLexeme",
    "NumeralLexeme",
]


class Lexeme:
    def __init__(
        self, value: str, form: InflectionForm, persistent_form: InflectionForm
    ) -> None:
        self._form = default_inflection_form()
        self._form.update(**form)
        self.value = value
        self.persistent_form = persistent_form

    @property
    def form(self):
        form = self._form.copy()
        form.update(**self.persistent_form)
        return form

    @form.setter
    def form(self, form):
        self._form.update(**form)

    def inflected(self, form: InflectionForm) -> "Lexeme":
        raise NotImplementedError()

    def text(self) -> str:
        raise NotImplementedError()


class DummyLexeme(Lexeme):
    def __init__(self, form: InflectionForm, persistent_form: InflectionForm) -> None:
        super().__init__("", form, persistent_form)

    def inflected(self, form: InflectionForm) -> "Lexeme":
        result = Lexeme("", self.form)
        result.form = form
        return result

    def text(self) -> str:  # pragma: no cover
        return ""

    def __repr__(self):  # pragma: no cover
        return "<empty>"


class ParadigmLexeme(Lexeme):
    def __init__(
        self,
        value,
        paradigm: List[Tuple[InflectionForm, str]],
        persistent_form: InflectionForm,
    ) -> None:
        super().__init__(
            value,
            default_inflection_form(),
            persistent_form,
        )
        self.paradigm = paradigm

    def inflected(self, form: InflectionForm) -> "Lexeme":
        result = ParadigmLexeme(self.value, self.paradigm, self.persistent_form)
        result.form = self.form
        result.form = form
        return result

    def text(self) -> str:
        for form, text in self.paradigm:
            if (
                (form.get("case", "") in ["", self.form["case"]])
                and (form.get("gender", "") in ["", self.form["gender"]])
                and (form.get("number", "") in ["", self.form["number"]])
                and (form.get("animacy", "") in ["", self.form["animacy"]])
            ):
                break
        else:
            raise InternalDataError()
        return text

    def __repr__(self):  # pragma: no cover
        return f"Lexeme<{self.value}>"


class CompoundOrdinalLexeme(ParadigmLexeme):
    def __init__(
        self,
        value: str,
        prefixes: List[str],
        paradigm: List[Tuple[InflectionForm, str]],
        persistent_form: InflectionForm,
    ) -> None:
        super().__init__(value, paradigm, persistent_form)
        self.cardinal_values = prefixes

    def text(self) -> str:
        return "".join([*self.cardinal_values[::-1], super().text()])

    def __repr__(self):  # pragma: no cover
        return f"CompoundLexeme<{self.value}>"


class NumeralLexeme:
    @staticmethod
    def cardinal(value: str) -> "Lexeme":
        return ParadigmLexeme(value, *cardinal.data[value])

    @staticmethod
    def ordinal(value: str) -> "Lexeme":
        return ParadigmLexeme(value, *ordinal.data[value])

    @staticmethod
    def ordinal_compound(cardinals_: List[str], ordinal_: str) -> "Lexeme":
        prefixes = [cardinal_stem.data[v][0][0][1] for v in cardinals_]
        ordinal_data = ordinal.data[ordinal_]
        value = str(sum(int(x) for x in [*cardinals_, ordinal_]))
        return CompoundOrdinalLexeme(value, prefixes, *ordinal_data)

    @staticmethod
    def misc(value: str) -> "Lexeme":
        return ParadigmLexeme(value, *misc.data[value])

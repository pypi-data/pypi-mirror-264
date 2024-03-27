from .lexeme import NumeralLexeme
from .grammar import *

cardinal = NumeralLexeme.cardinal


# fmt: off
def test_nominative():
    form = {"case": Case.nominative}
    assert cardinal("1").inflected(form).text() == "оди́н"
    assert cardinal("4").inflected(form).text() == "чоти́ри"
    assert cardinal("5").inflected(form).text() == "пʼя́ть"
    assert cardinal("6").inflected(form).text() == "ші́сть"
    assert cardinal("8").inflected(form).text() == "ві́сім"
    assert cardinal("9").inflected(form).text() == "де́вʼять"
    assert cardinal("10").inflected(form).text() == "де́сять"
    assert cardinal("11").inflected(form).text() == "одина́дцять"
    assert cardinal("15").inflected(form).text() == "пʼятна́дцять"
    assert cardinal("16").inflected(form).text() == "шістна́дцять"
    assert cardinal("18").inflected(form).text() == "вісімна́дцять"
    assert cardinal("19").inflected(form).text() == "девʼятна́дцять"
    assert cardinal("20").inflected(form).text() == "два́дцять"
    assert cardinal("30").inflected(form).text() == "три́дцять"
    assert cardinal("100").inflected(form).text() == "сто́"


def test_genitive():
    form = {"case": Case.genitive}
    assert cardinal("1").inflected(form).text() == "одного́"
    assert cardinal("2").inflected(form).text() == "дво́х"
    assert cardinal("3").inflected(form).text() == "трьо́х"
    assert cardinal("4").inflected(form).text() == "чотирьо́х"
    assert cardinal("5").inflected(form).text() == "пʼяти́"
    assert cardinal("6").inflected(form).text() == "шести́"
    assert cardinal("7").inflected(form).text() == "семи́"
    assert cardinal("8").inflected(form).text() == "восьми́"
    assert cardinal("9").inflected(form).text() == "девʼяти́"
    assert cardinal("10").inflected(form).text() == "десяти́"
    assert cardinal("11").inflected(form).text() == "одинадцяти́"
    assert cardinal("12").inflected(form).text() == "дванадцяти́"
    assert cardinal("13").inflected(form).text() == "тринадцяти́"
    assert cardinal("14").inflected(form).text() == "чотирнадцяти́"
    assert cardinal("15").inflected(form).text() == "пʼятнадцяти́"
    assert cardinal("16").inflected(form).text() == "шістнадцяти́"
    assert cardinal("17").inflected(form).text() == "сімнадцяти́"
    assert cardinal("18").inflected(form).text() == "вісімнадцяти́"
    assert cardinal("19").inflected(form).text() == "девʼятнадцяти́"
    assert cardinal("20").inflected(form).text() == "двадцяти́"
    assert cardinal("30").inflected(form).text() == "тридцяти́"
    assert cardinal("100").inflected(form).text() == "ста́"


def test_dative():
    form = {"case": Case.dative, "gender": Gender.masculine}
    assert cardinal("1").inflected(form).text() == "одному́"
    assert cardinal("4").inflected(form).text() == "чотирьо́м"
    assert cardinal("5").inflected(form).text() == "пʼяти́"
    assert cardinal("6").inflected(form).text() == "шести́"
    assert cardinal("8").inflected(form).text() == "восьми́"
    assert cardinal("9").inflected(form).text() == "девʼяти́"
    assert cardinal("10").inflected(form).text() == "десяти́"
    assert cardinal("11").inflected(form).text() == "одинадцяти́"
    assert cardinal("15").inflected(form).text() == "пʼятнадцяти́"
    assert cardinal("16").inflected(form).text() == "шістнадцяти́"
    assert cardinal("18").inflected(form).text() == "вісімнадцяти́"
    assert cardinal("19").inflected(form).text() == "девʼятнадцяти́"
    assert cardinal("20").inflected(form).text() == "двадцяти́"
    assert cardinal("30").inflected(form).text() == "тридцяти́"
    assert cardinal("100").inflected(form).text() == "ста́"


def test_accusative():
    form = {"case": Case.accusative}
    assert cardinal("1").inflected(form).text() == "оди́н"
    assert cardinal("4").inflected(form).text() == "чоти́ри"
    assert cardinal("5").inflected(form).text() == "пʼя́ть"
    assert cardinal("6").inflected(form).text() == "ші́сть"
    assert cardinal("8").inflected(form).text() == "ві́сім"
    assert cardinal("9").inflected(form).text() == "де́вʼять"
    assert cardinal("10").inflected(form).text() == "де́сять"
    assert cardinal("11").inflected(form).text() == "одина́дцять"
    assert cardinal("15").inflected(form).text() == "пʼятна́дцять"
    assert cardinal("16").inflected(form).text() == "шістна́дцять"
    assert cardinal("18").inflected(form).text() == "вісімна́дцять"
    assert cardinal("19").inflected(form).text() == "девʼятна́дцять"
    assert cardinal("20").inflected(form).text() == "два́дцять"
    assert cardinal("30").inflected(form).text() == "три́дцять"
    assert cardinal("100").inflected(form).text() == "сто́"


def test_instrumental():
    form = {"case": Case.instrumental}
    assert cardinal("1").inflected(form).text() == "одни́м"
    assert cardinal("4").inflected(form).text() == "чотирма́"
    assert cardinal("5").inflected(form).text() == "пʼятьма́"
    assert cardinal("6").inflected(form).text() == "шістьма́"
    assert cardinal("8").inflected(form).text() == "вісьма́"
    assert cardinal("9").inflected(form).text() == "девʼятьма́"
    assert cardinal("10").inflected(form).text() == "десятьма́"
    assert cardinal("11").inflected(form).text() == "одинадцятьма́"
    assert cardinal("15").inflected(form).text() == "пʼятнадцятьма́"
    assert cardinal("16").inflected(form).text() == "шістнадцятьма́"
    assert cardinal("18").inflected(form).text() == "вісімнадцятьма́"
    assert cardinal("19").inflected(form).text() == "девʼятнадцятьма́"
    assert cardinal("20").inflected(form).text() == "двадцятьма́"
    assert cardinal("30").inflected(form).text() == "тридцятьма́"
    assert cardinal("100").inflected(form).text() == "ста́"


def test_locative():
    form = {"case": Case.locative, "gender": Gender.masculine}
    assert cardinal("1").inflected(form).text() == "одному́"
    assert cardinal("4").inflected(form).text() == "чотирьо́х"
    assert cardinal("5").inflected(form).text() == "пʼяти́"
    assert cardinal("6").inflected(form).text() == "шести́"
    assert cardinal("8").inflected(form).text() == "восьми́"
    assert cardinal("9").inflected(form).text() == "девʼяти́"
    assert cardinal("10").inflected(form).text() == "десяти́"
    assert cardinal("11").inflected(form).text() == "одинадцяти́"
    assert cardinal("15").inflected(form).text() == "пʼятнадцяти́"
    assert cardinal("16").inflected(form).text() == "шістнадцяти́"
    assert cardinal("19").inflected(form).text() == "девʼятнадцяти́"
    assert cardinal("20").inflected(form).text() == "двадцяти́"
    assert cardinal("30").inflected(form).text() == "тридцяти́"
    assert cardinal("100").inflected(form).text() == "ста́"

def test_vocative():
    form = {"case": Case.vocative, "gender": Gender.masculine}
    assert cardinal("1").inflected(form).text() == "оди́н"
    assert cardinal("4").inflected(form).text() == "чоти́ри"
    assert cardinal("5").inflected(form).text() == "пʼя́ть"
    assert cardinal("6").inflected(form).text() == "ші́сть"
    assert cardinal("8").inflected(form).text() == "ві́сім"
    assert cardinal("9").inflected(form).text() == "де́вʼять"
    assert cardinal("10").inflected(form).text() == "де́сять"
    assert cardinal("11").inflected(form).text() == "одина́дцять"
    assert cardinal("15").inflected(form).text() == "пʼятна́дцять"
    assert cardinal("16").inflected(form).text() == "шістна́дцять"
    assert cardinal("18").inflected(form).text() == "вісімна́дцять"
    assert cardinal("19").inflected(form).text() == "девʼятна́дцять"
    assert cardinal("20").inflected(form).text() == "два́дцять"
    assert cardinal("30").inflected(form).text() == "три́дцять"
    assert cardinal("100").inflected(form).text() == "сто́"


def test_noun_nominative():
    form = {"case": Case.nominative}
    assert cardinal("1000").inflected(form).text() == "ти́сяча"
    assert cardinal("1000000").inflected(form).text() == "мільйо́н"


def test_noun_genitive():
    form = {"case": Case.genitive}
    assert cardinal("1000").inflected(form).text() == "ти́сячі"
    assert cardinal("1000000").inflected(form).text() == "мільйо́на"


def test_noun_dative():
    form = {"case": Case.dative, "gender": Gender.masculine}
    assert cardinal("1000").inflected(form).text() == "ти́сячі"
    assert cardinal("1000000").inflected(form).text() == "мільйо́ну"


def test_noun_accusative():
    form = {"case": Case.accusative}
    assert cardinal("1000").inflected(form).text() == "ти́сячу"
    assert cardinal("1000000").inflected(form).text() == "мільйо́н"


def test_noun_instrumental():
    form = {"case": Case.instrumental}
    assert cardinal("1000").inflected(form).text() == "ти́сячею"
    assert cardinal("1000000").inflected(form).text() == "мільйо́ном"


def test_noun_locative():
    form = {"case": Case.locative, "gender": Gender.masculine}
    assert cardinal("1000").inflected(form).text() == "ти́сячі"
    assert cardinal("1000000").inflected(form).text() == "мільйо́ні"


def test_noun_vocative():
    form = {"case": Case.vocative, "gender": Gender.masculine}
    assert cardinal("1000").inflected(form).text() == "ти́сяче"
    assert cardinal("1000000").inflected(form).text() == "мільйо́не"


# fmt: on

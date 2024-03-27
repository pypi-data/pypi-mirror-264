import pytest
from .cardinals import inflect
from .errors import RangeError


# fmt: off
simple_map = {
    "nom": ("case", "nominative"),
    "gen": ("case", "genitive"),
    "dat": ("case", "dative"),
    "acc": ("case", "accusative"),
    "inst": ("case", "instrumental"),
    "loc": ("case", "locative"),
    "voc": ("case", "vocative"),
    "m": ("gender", "masculine"),
    "f": ("gender", "feminine"),
    "n": ("gender", "neuter"),
    "sg": ("number", "singular"),
    "pl": ("number", "plural"),
    "card": ("type", "cardinal"),
    "ord": ("type", "ordinal"),
    "inan": ("animacy", "inanimate"),
    "anim": ("animacy", "animate"),
}


def fm(s):
    return {simple_map[g][0]: simple_map[g][1] for g in s.split(";")}


def test_0():
    assert inflect("0", fm("m")) == "ну́ль"
    assert inflect("0", fm("f")) == "ну́ль"
    assert inflect("0", fm("n")) == "ну́ль"
    assert inflect("0", fm("gen")) == "нуля́"
    assert inflect("0", fm("gen;f")) == "нуля́"
    assert inflect("0", fm("acc;f;anim")) == "ну́ль"
    assert inflect("0", fm("acc;f;inan")) == "ну́ль"
    assert inflect("0", fm("loc;f")) == "нулі́"


def test_lpad_0():
    assert inflect("00", fm("m")) == "ну́ль"
    assert inflect("000000", fm("m")) == "ну́ль"
    assert inflect("021", fm("m")) == "два́дцять оди́н"
    assert inflect("0000000021", fm("m")) == "два́дцять оди́н"


def test_21():
    assert inflect("21", fm("m")) == "два́дцять оди́н"
    assert inflect("21", fm("f")) == "два́дцять одна́"
    assert inflect("21", fm("n")) == "два́дцять одне́"
    assert inflect("21", fm("gen")) == "двадцяти́ одного́"
    assert inflect("21", fm("gen;f")) == "двадцяти́ одніє́ї"
    assert inflect("21", fm("acc;f;anim")) == "двадцятьо́х одну́"
    assert inflect("21", fm("acc;f;inan")) == "два́дцять одну́"
    assert inflect("21", fm("loc;f")) == "двадцяти́ одні́й"


def test_34():
    assert inflect("34", fm("m")) == "три́дцять чоти́ри"
    assert inflect("34", fm("f")) == "три́дцять чоти́ри"
    assert inflect("34", fm("n")) == "три́дцять чоти́ри"
    assert inflect("34", fm("gen")) == "тридцяти́ чотирьо́х"
    assert inflect("34", fm("gen;f")) == "тридцяти́ чотирьо́х"
    assert inflect("34", fm("acc;f;anim")) == "тридцятьо́х чотирьо́х"
    assert inflect("34", fm("acc;f;inan")) == "три́дцять чоти́ри"
    assert inflect("34", fm("loc;f")) == "тридцяти́ чотирьо́х"


def test_713():
    assert inflect("713", fm("m")) == "сімсо́т трина́дцять"
    assert inflect("713", fm("f")) == "сімсо́т трина́дцять"
    assert inflect("713", fm("n")) == "сімсо́т трина́дцять"
    assert inflect("713", fm("gen")) == "семисо́т тринадцяти́"
    assert inflect("713", fm("gen;f")) == "семисо́т тринадцяти́"
    assert inflect("713", fm("acc;f;anim")) == "сімсо́т тринадцятьо́х"
    assert inflect("713", fm("acc;f;inan")) == "сімсо́т трина́дцять"
    assert inflect("713", fm("loc;f")) == "семиста́х тринадцяти́"


def test_999():
    assert inflect("999", fm("m")) == "девʼятсо́т девʼяно́сто де́вʼять"
    assert inflect("999", fm("f")) == "девʼятсо́т девʼяно́сто де́вʼять"
    assert inflect("999", fm("n")) == "девʼятсо́т девʼяно́сто де́вʼять"
    assert inflect("999", fm("gen")) == "девʼятисо́т девʼяно́ста девʼяти́"
    assert inflect("999", fm("gen;f")) == "девʼятисо́т девʼяно́ста девʼяти́"
    assert inflect("999", fm("acc;f;anim")) == "девʼятсо́т девʼяно́сто девʼятьо́х"
    assert inflect("999", fm("acc;f;inan")) == "девʼятсо́т девʼяно́сто де́вʼять"
    assert inflect("999", fm("loc;f")) == "девʼятиста́х девʼяно́ста девʼяти́"


def test_1000():
    assert inflect("1000", fm("m")) == "ти́сяча"
    assert inflect("1000", fm("f")) == "ти́сяча"
    assert inflect("1000", fm("n")) == "ти́сяча"
    assert inflect("1000", fm("gen;m")) == "ти́сячі"
    assert inflect("1000", fm("gen;f")) == "ти́сячі"
    assert inflect("1000", fm("dat")) == "ти́сячі"
    assert inflect("1000", fm("acc")) == "ти́сячу"
    assert inflect("1000", fm("acc;f;anim")) == "ти́сячу"
    assert inflect("1000", fm("acc;f;inan")) == "ти́сячу"
    assert inflect("1000", fm("loc;f")) == "ти́сячі"
    assert inflect("1000", fm("loc")) == "ти́сячі"
    assert inflect("1000", fm("inst")) == "ти́сячею"


def test_1000_insert_ones():
    assert inflect("1000", fm("m"), insert_ones=True) == "одна́ ти́сяча"
    assert inflect("1000", fm("f"), insert_ones=True) == "одна́ ти́сяча"
    assert inflect("1000", fm("n"), insert_ones=True) == "одна́ ти́сяча"
    assert inflect("1000", fm("gen;m"), insert_ones=True) == "одніє́ї ти́сячі"
    assert inflect("1000", fm("gen;f"), insert_ones=True) == "одніє́ї ти́сячі"
    assert inflect("1000", fm("dat"), insert_ones=True) == "одні́й ти́сячі"
    assert inflect("1000", fm("acc"), insert_ones=True) == "одну́ ти́сячу"
    assert inflect("1000", fm("acc;f;anim"), insert_ones=True) == "одну́ ти́сячу"
    assert inflect("1000", fm("acc;f;inan"), insert_ones=True) == "одну́ ти́сячу"
    assert inflect("1000", fm("loc;f"), insert_ones=True) == "одні́й ти́сячі"
    assert inflect("1000", fm("loc"), insert_ones=True) == "одні́й ти́сячі"
    assert inflect("1000", fm("inst"), insert_ones=True) == "одніє́ю ти́сячею"


def test_4486():
    assert inflect("4486", fm("m")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т ші́сть"
    assert inflect("4486", fm("f")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т ші́сть"
    assert inflect("4486", fm("n")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т ші́сть"
    assert inflect("4486", fm("gen")) == "чотирьо́х ти́сяч чотирьохсо́т вісімдесяти́ шести́"
    assert inflect("4486", fm("gen;f")) == "чотирьо́х ти́сяч чотирьохсо́т вісімдесяти́ шести́"
    assert inflect("4486", fm("acc;f;anim")) == "чоти́ри ти́сячі чоти́риста вісімдесятьо́х шістьо́х"
    assert inflect("4486", fm("acc;f;inan")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т ші́сть"
    assert inflect("4486", fm("loc;f")) == "чотирьо́х ти́сячах чотирьохста́х вісімдесяти́ шести́"


def test_1000000():
    assert inflect("1000000", fm("nom")) == "мільйо́н"
    assert inflect("1000000", fm("gen")) == "мільйо́на"
    assert inflect("1000000", fm("dat")) == "мільйо́ну"
    assert inflect("1000000", fm("acc")) == "мільйо́н"
    assert inflect("1000000", fm("inst")) == "мільйо́ном"
    assert inflect("1000000", fm("loc")) == "мільйо́ні"


def test_1000000_insert_ones():
    assert inflect("1000000", fm("nom"), insert_ones=True) == "оди́н мільйо́н"
    assert inflect("1000000", fm("gen"), insert_ones=True) == "одного́ мільйо́на"
    assert inflect("1000000", fm("dat"), insert_ones=True) == "одному́ мільйо́ну"
    assert inflect("1000000", fm("acc"), insert_ones=True) == "оди́н мільйо́н"
    assert inflect("1000000", fm("inst"), insert_ones=True) == "одни́м мільйо́ном"
    assert inflect("1000000", fm("loc"), insert_ones=True) == "одному́ мільйо́ні"


def test_801066():
    assert inflect("801066", fm("nom")) == "вісімсо́т одна́ ти́сяча шістдеся́т ші́сть"
    assert inflect("801066", fm("gen")) == "восьмисо́т одніє́ї ти́сячі шістдесяти́ шести́"
    assert inflect("801066", fm("dat")) == "восьмиста́м одні́й ти́сячі шістдесяти́ шести́"
    assert inflect("801066", fm("acc")) == "вісімсо́т одну́ ти́сячу шістдеся́т ші́сть"
    assert inflect("801066", fm("inst")) == "вісьмаста́ми одніє́ю ти́сячею шістдесятьма́ шістьма́"
    assert inflect("801066", fm("loc")) == "восьмиста́х одні́й ти́сячі шістдесяти́ шести́"


def test_5178030():
    assert inflect("5178030", fm("m")) == "пʼя́ть мільйо́нів сто́ сімдеся́т ві́сім ти́сяч три́дцять"
    assert inflect("5178030", fm("f")) == "пʼя́ть мільйо́нів сто́ сімдеся́т ві́сім ти́сяч три́дцять"
    assert inflect("5178030", fm("n")) == "пʼя́ть мільйо́нів сто́ сімдеся́т ві́сім ти́сяч три́дцять"
    assert inflect("5178030", fm("gen")) == "пʼяти́ мільйо́нів ста́ сімдесяти́ восьми́ ти́сяч тридцяти́"
    assert inflect("5178030", fm("gen;f")) == "пʼяти́ мільйо́нів ста́ сімдесяти́ восьми́ ти́сяч тридцяти́"
    assert inflect("5178030", fm("acc;f;anim")) == "пʼя́ть мільйо́нів сто́ сімдеся́т ві́сім ти́сяч тридцятьо́х"
    assert inflect("5178030", fm("acc;f;inan")) == "пʼя́ть мільйо́нів сто́ сімдеся́т ві́сім ти́сяч три́дцять"
    assert inflect("5178030", fm("loc;f")) == "пʼяти́ мільйо́нах ста́ сімдесяти́ восьми́ ти́сячах тридцяти́"


def test_488108826177873():
    assert inflect("488108826177873", fm("m")) == "чоти́риста вісімдеся́т ві́сім трильйо́нів сто́ ві́сім мілья́рдів вісімсо́т два́дцять ші́сть мільйо́нів сто́ сімдеся́т сі́м ти́сяч вісімсо́т сімдеся́т три́"
    assert inflect("488108826177873", fm("f")) == "чоти́риста вісімдеся́т ві́сім трильйо́нів сто́ ві́сім мілья́рдів вісімсо́т два́дцять ші́сть мільйо́нів сто́ сімдеся́т сі́м ти́сяч вісімсо́т сімдеся́т три́"
    assert inflect("488108826177873", fm("n")) == "чоти́риста вісімдеся́т ві́сім трильйо́нів сто́ ві́сім мілья́рдів вісімсо́т два́дцять ші́сть мільйо́нів сто́ сімдеся́т сі́м ти́сяч вісімсо́т сімдеся́т три́"
    assert inflect("488108826177873", fm("gen")) == "чотирьохсо́т вісімдесяти́ восьми́ трильйо́нів ста́ восьми́ мілья́рдів восьмисо́т двадцяти́ шести́ мільйо́нів ста́ сімдесяти́ семи́ ти́сяч восьмисо́т сімдесяти́ трьо́х"
    assert inflect("488108826177873", fm("gen;f")) == "чотирьохсо́т вісімдесяти́ восьми́ трильйо́нів ста́ восьми́ мілья́рдів восьмисо́т двадцяти́ шести́ мільйо́нів ста́ сімдесяти́ семи́ ти́сяч восьмисо́т сімдесяти́ трьо́х", "genitive, feminine"
    assert inflect("488108826177873", fm("acc;f;anim")) == "чоти́риста вісімдеся́т ві́сім трильйо́нів сто́ ві́сім мілья́рдів вісімсо́т два́дцять ші́сть мільйо́нів сто́ сімдеся́т сі́м ти́сяч вісімсо́т сімдесятьо́х трьо́х"
    assert inflect("488108826177873", fm("acc;f;inan")) == "чоти́риста вісімдеся́т ві́сім трильйо́нів сто́ ві́сім мілья́рдів вісімсо́т два́дцять ші́сть мільйо́нів сто́ сімдеся́т сі́м ти́сяч вісімсо́т сімдеся́т три́"
    assert inflect("488108826177873", fm("loc;f")) == "чотирьохста́х вісімдесяти́ восьми́ трильйо́нах ста́ восьми́ мілья́рдах восьмиста́х двадцяти́ шести́ мільйо́нах ста́ сімдесяти́ семи́ ти́сячах восьмиста́х сімдесяти́ трьо́х", "locative, feminine"


def test_591359027947837343695787388():
    assert inflect("591359027947837343695787388", fm("nom;m")) == "пʼятсо́т девʼяно́сто оди́н септильйо́н три́ста пʼятдеся́т де́вʼять секстильйо́нів два́дцять сі́м квінтильйо́нів девʼятсо́т со́рок сі́м квадрильйо́нів вісімсо́т три́дцять сі́м трильйо́нів три́ста со́рок три́ мілья́рди шістсо́т девʼяно́сто пʼя́ть мільйо́нів сімсо́т вісімдеся́т сі́м ти́сяч три́ста вісімдеся́т ві́сім"


def test_nominative():
    assert inflect("0", fm("nom")) == "ну́ль"
    assert inflect("1", fm("nom")) == "оди́н"
    assert inflect("4", fm("nom")) == "чоти́ри"
    assert inflect("5", fm("nom")) == "пʼя́ть"
    assert inflect("6", fm("nom")) == "ші́сть"
    assert inflect("8", fm("nom")) == "ві́сім"
    assert inflect("9", fm("nom")) == "де́вʼять"
    assert inflect("10", fm("nom")) == "де́сять"
    assert inflect("11", fm("nom")) == "одина́дцять"
    assert inflect("15", fm("nom")) == "пʼятна́дцять"
    assert inflect("16", fm("nom")) == "шістна́дцять"
    assert inflect("18", fm("nom")) == "вісімна́дцять"
    assert inflect("19", fm("nom")) == "девʼятна́дцять"
    assert inflect("20", fm("nom")) == "два́дцять"
    assert inflect("30", fm("nom")) == "три́дцять"
    assert inflect("100", fm("nom")) == "сто́"


def test_genitive():
    assert inflect("0", fm("gen")) == "нуля́"
    assert inflect("1", fm("gen")) == "одного́"
    assert inflect("2", fm("gen")) == "дво́х"
    assert inflect("3", fm("gen")) == "трьо́х"
    assert inflect("4", fm("gen")) == "чотирьо́х"
    assert inflect("5", fm("gen")) == "пʼяти́"
    assert inflect("6", fm("gen")) == "шести́"
    assert inflect("7", fm("gen")) == "семи́"
    assert inflect("8", fm("gen")) == "восьми́"
    assert inflect("9", fm("gen")) == "девʼяти́"
    assert inflect("10", fm("gen")) == "десяти́"
    assert inflect("11", fm("gen")) == "одинадцяти́"
    assert inflect("12", fm("gen")) == "дванадцяти́"
    assert inflect("13", fm("gen")) == "тринадцяти́"
    assert inflect("14", fm("gen")) == "чотирнадцяти́"
    assert inflect("15", fm("gen")) == "пʼятнадцяти́"
    assert inflect("16", fm("gen")) == "шістнадцяти́"
    assert inflect("17", fm("gen")) == "сімнадцяти́"
    assert inflect("18", fm("gen")) == "вісімнадцяти́"
    assert inflect("19", fm("gen")) == "девʼятнадцяти́"
    assert inflect("20", fm("gen")) == "двадцяти́"
    assert inflect("30", fm("gen")) == "тридцяти́"
    assert inflect("100", fm("gen")) == "ста́"


def test_dative():
    assert inflect("0", fm("dat")) == "нулю́"
    assert inflect("1", fm("dat")) == "одному́"
    assert inflect("4", fm("dat")) == "чотирьо́м"
    assert inflect("5", fm("dat")) == "пʼяти́"
    assert inflect("6", fm("dat")) == "шести́"
    assert inflect("8", fm("dat")) == "восьми́"
    assert inflect("9", fm("dat")) == "девʼяти́"
    assert inflect("10", fm("dat")) == "десяти́"
    assert inflect("11", fm("dat")) == "одинадцяти́"
    assert inflect("15", fm("dat")) == "пʼятнадцяти́"
    assert inflect("16", fm("dat")) == "шістнадцяти́"
    assert inflect("18", fm("dat")) == "вісімнадцяти́"
    assert inflect("19", fm("dat")) == "девʼятнадцяти́"
    assert inflect("20", fm("dat")) == "двадцяти́"
    assert inflect("30", fm("dat")) == "тридцяти́"
    assert inflect("100", fm("dat")) == "ста́"


def test_accusative():
    assert inflect("0", fm("acc")) == "ну́ль"
    assert inflect("1", fm("acc")) == "оди́н"
    assert inflect("4", fm("acc")) == "чоти́ри"
    assert inflect("5", fm("acc")) == "пʼя́ть"
    assert inflect("6", fm("acc")) == "ші́сть"
    assert inflect("8", fm("acc")) == "ві́сім"
    assert inflect("9", fm("acc")) == "де́вʼять"
    assert inflect("10", fm("acc")) == "де́сять"
    assert inflect("11", fm("acc")) == "одина́дцять"
    assert inflect("15", fm("acc")) == "пʼятна́дцять"
    assert inflect("16", fm("acc")) == "шістна́дцять"
    assert inflect("18", fm("acc")) == "вісімна́дцять"
    assert inflect("19", fm("acc")) == "девʼятна́дцять"
    assert inflect("20", fm("acc")) == "два́дцять"
    assert inflect("30", fm("acc")) == "три́дцять"
    assert inflect("100", fm("acc")) == "сто́"


def test_instrumental():
    assert inflect("0", fm("inst")) == "нуле́м"
    assert inflect("1", fm("inst")) == "одни́м"
    assert inflect("4", fm("inst")) == "чотирма́"
    assert inflect("5", fm("inst")) == "пʼятьма́"
    assert inflect("6", fm("inst")) == "шістьма́"
    assert inflect("8", fm("inst")) == "вісьма́"
    assert inflect("9", fm("inst")) == "девʼятьма́"
    assert inflect("10", fm("inst")) == "десятьма́"
    assert inflect("11", fm("inst")) == "одинадцятьма́"
    assert inflect("15", fm("inst")) == "пʼятнадцятьма́"
    assert inflect("16", fm("inst")) == "шістнадцятьма́"
    assert inflect("18", fm("inst")) == "вісімнадцятьма́"
    assert inflect("19", fm("inst")) == "девʼятнадцятьма́"
    assert inflect("20", fm("inst")) == "двадцятьма́"
    assert inflect("30", fm("inst")) == "тридцятьма́"
    assert inflect("100", fm("inst")) == "ста́"


def test_locative():
    assert inflect("0", fm("loc")) == "нулі́"
    assert inflect("1", fm("loc")) == "одному́"
    assert inflect("4", fm("loc")) == "чотирьо́х"
    assert inflect("5", fm("loc")) == "пʼяти́"
    assert inflect("6", fm("loc")) == "шести́"
    assert inflect("8", fm("loc")) == "восьми́"
    assert inflect("9", fm("loc")) == "девʼяти́"
    assert inflect("10", fm("loc")) == "десяти́"
    assert inflect("11", fm("loc")) == "одинадцяти́"
    assert inflect("15", fm("loc")) == "пʼятнадцяти́"
    assert inflect("16", fm("loc")) == "шістнадцяти́"
    assert inflect("19", fm("loc")) == "девʼятнадцяти́"
    assert inflect("20", fm("loc")) == "двадцяти́"
    assert inflect("30", fm("loc")) == "тридцяти́"
    assert inflect("100", fm("loc")) == "ста́"



def test_vocative():
    assert inflect("0", fm("voc")) == "ну́лю"
    assert inflect("1", fm("voc")) == "оди́н"
    assert inflect("4", fm("voc")) == "чоти́ри"
    assert inflect("5", fm("voc")) == "пʼя́ть"
    assert inflect("6", fm("voc")) == "ші́сть"
    assert inflect("8", fm("voc")) == "ві́сім"
    assert inflect("9", fm("voc")) == "де́вʼять"
    assert inflect("10", fm("voc")) == "де́сять"
    assert inflect("11", fm("voc")) == "одина́дцять"
    assert inflect("15", fm("voc")) == "пʼятна́дцять"
    assert inflect("16", fm("voc")) == "шістна́дцять"
    assert inflect("18", fm("voc")) == "вісімна́дцять"
    assert inflect("19", fm("voc")) == "девʼятна́дцять"
    assert inflect("20", fm("voc")) == "два́дцять"
    assert inflect("30", fm("voc")) == "три́дцять"
    assert inflect("100", fm("voc")) == "сто́"

def test_all_neuter():
    f = fm("inst;n")
    assert inflect("1", f) == "одни́м"
    assert inflect("2", f) == "двома́"
    assert inflect("3", f) == "трьома́"
    assert inflect("4", f) == "чотирма́"
    assert inflect("5", f) == "пʼятьма́"
    assert inflect("6", f) == "шістьма́"
    assert inflect("7", f) == "сьома́"
    assert inflect("8", f) == "вісьма́"
    assert inflect("9", f) == "девʼятьма́"
    assert inflect("11", f) == "одинадцятьма́"
    assert inflect("12", f) == "дванадцятьма́"
    assert inflect("13", f) == "тринадцятьма́"
    assert inflect("14", f) == "чотирнадцятьма́"
    assert inflect("15", f) == "пʼятнадцятьма́"
    assert inflect("16", f) == "шістнадцятьма́"
    assert inflect("17", f) == "сімнадцятьма́"
    assert inflect("18", f) == "вісімнадцятьма́"
    assert inflect("19", f) == "девʼятнадцятьма́"
    assert inflect("10", f) == "десятьма́"
    assert inflect("20", f) == "двадцятьма́"
    assert inflect("30", f) == "тридцятьма́"
    assert inflect("40", f) == "сорока́"
    assert inflect("50", f) == "пʼятдесятьма́"
    assert inflect("60", f) == "шістдесятьма́"
    assert inflect("70", f) == "сімдесятьма́"
    assert inflect("80", f) == "вісімдесятьма́"
    assert inflect("90", f) == "девʼяно́ста"
    assert inflect("100", f) == "ста́"
    assert inflect("200", f) == "двомаста́ми"
    assert inflect("300", f) == "трьомаста́ми"
    assert inflect("400", f) == "чотирмаста́ми"
    assert inflect("500", f) == "пʼятьмаста́ми"
    assert inflect("600", f) == "шістьмаста́ми"
    assert inflect("700", f) == "семиста́ми"
    assert inflect("800", f) == "вісьмаста́ми"
    assert inflect("900", f) == "девʼятьмаста́ми"


def test_range_fallback():
    assert inflect("999999999999999999999999999", fm("m")) == "девʼятсо́т девʼяно́сто де́вʼять септильйо́нів девʼятсо́т девʼяно́сто де́вʼять секстильйо́нів девʼятсо́т девʼяно́сто де́вʼять квінтильйо́нів девʼятсо́т девʼяно́сто де́вʼять квадрильйо́нів девʼятсо́т девʼяно́сто де́вʼять трильйо́нів девʼятсо́т девʼяно́сто де́вʼять мілья́рдів девʼятсо́т девʼяно́сто де́вʼять мільйо́нів девʼятсо́т девʼяно́сто де́вʼять ти́сяч девʼятсо́т девʼяно́сто де́вʼять"
    assert inflect("1000000000000000000000000000", fm("m")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль"
    assert inflect("1000000000000000000000000001", fm("m")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль оди́н"
    assert inflect("1234567890123456789012345678", fm("m")) == "оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім"
    assert inflect("999999999999999999999999999", fm("f")) == "девʼятсо́т девʼяно́сто де́вʼять септильйо́нів девʼятсо́т девʼяно́сто де́вʼять секстильйо́нів девʼятсо́т девʼяно́сто де́вʼять квінтильйо́нів девʼятсо́т девʼяно́сто де́вʼять квадрильйо́нів девʼятсо́т девʼяно́сто де́вʼять трильйо́нів девʼятсо́т девʼяно́сто де́вʼять мілья́рдів девʼятсо́т девʼяно́сто де́вʼять мільйо́нів девʼятсо́т девʼяно́сто де́вʼять ти́сяч девʼятсо́т девʼяно́сто де́вʼять"
    assert inflect("1000000000000000000000000000", fm("f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль"
    assert inflect("1000000000000000000000000001", fm("f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль одна́"
    assert inflect("1234567890123456789012345678", fm("f")) == "оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім"
    assert inflect("1000000000000000000000000000", fm("gen;f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль нуля́"
    assert inflect("1000000000000000000000000001", fm("gen;f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль одніє́ї"


def test_strict_range():
    assert inflect("999999999999999999999999999", fm("m"), strict_range=True)
    with pytest.raises(RangeError):
        assert inflect("1000000000000000000000000000", fm("m"), strict_range=True)


def test_insert_ones():
    assert inflect("100", fm("m"), insert_ones=True) == "сто́"
    assert inflect("101", fm("m"), insert_ones=True) == "сто́ оди́н"
    assert inflect("1000", fm("m"), insert_ones=True) == "одна́ ти́сяча"
    assert inflect("1001", fm("m"), insert_ones=True) == "одна́ ти́сяча оди́н"
    assert inflect("1000000", fm("m"), insert_ones=True) == "оди́н мільйо́н"
    assert inflect("1000001", fm("m"), insert_ones=True) == "оди́н мільйо́н оди́н"
    assert inflect("100", fm("m"), insert_ones=True) == "сто́"
    assert inflect("101", fm("f"), insert_ones=True) == "сто́ одна́"
    assert inflect("1000", fm("f"), insert_ones=True) == "одна́ ти́сяча"
    assert inflect("1001", fm("f"), insert_ones=True) == "одна́ ти́сяча одна́"
    assert inflect("1000000", fm("f"), insert_ones=True) == "оди́н мільйо́н"
    assert inflect("1000001", fm("f"), insert_ones=True) == "оди́н мільйо́н одна́"


"""
Numbers to also test:
2
3
7
12
13
14
42
71
28
31
35
51
38
71
101
104
105
109
1001
4486
9999
100000
803066
999999
1000001
9999999
100000000
857049589
999999999
1000000000
1000000000000
488108826177873
999999999999999
"""

# fmt: on

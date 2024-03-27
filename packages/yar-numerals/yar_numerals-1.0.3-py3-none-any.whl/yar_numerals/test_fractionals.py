import pytest
from .fractionals import inflect
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


# def test_0():
#     assert inflect("0", "0" fm("m")) == "нульови́й"
#     assert inflect("0", fm("f")) == "нульова́"
#     assert inflect("0", fm("n")) == "нульове́"
#     assert inflect("0", fm("gen")) == "нульово́го"
#     assert inflect("0", fm("gen;f")) == "нульово́ї"
#     assert inflect("0", fm("acc;f;anim")) == "нульову́"
#     assert inflect("0", fm("acc;f;inan")) == "нульову́"
#     assert inflect("0", fm("loc;f")) == "нульові́й"


def test_gov_agreement():
    assert inflect("", "1", "1", fm("m")) == "одна́ пе́рша"
    assert inflect("", "2", "1", fm("m")) == "дві́ пе́рших"
    assert inflect("", "3", "1", fm("m")) == "три́ пе́рших"
    assert inflect("", "5", "1", fm("m")) == "пʼя́ть пе́рших"
    assert inflect("", "0", "1", fm("m")) == "ну́ль пе́рших"

def test_1_2():
    assert inflect("", "1", "2", fm("m")) == "одна́ дру́га"
    assert inflect("", "1", "2", fm("gen;m")) == "одніє́ї дру́гої"
    assert inflect("", "1", "2", fm("acc;m")) == "одну́ дру́гу"
    assert inflect("", "1", "2", fm("dat;m")) == "одні́й дру́гій"
    assert inflect("", "1", "2", fm("inst;m")) == "одніє́ю дру́гою"
    assert inflect("", "1", "2", fm("loc;m")) == "одні́й дру́гій"
    assert inflect("", "1", "2", fm("voc;m")) == "одна́ дру́га"

def test_40_143():
    assert inflect("", "40", "143", fm("m")) == "со́рок сто́ со́рок тре́тіх"

def test_1_1_2():
    assert inflect("1", "1", "2", fm("m")) == "одна́ ці́ла одна́ дру́га"
    assert inflect("1", "1", "2", fm("m;gen")) == "одніє́ї ці́лої одніє́ї дру́гої"

def test_1002_1003():
    assert inflect("", "1002", "1003", fm("nom;m")) == "ти́сяча дві́ ти́сяча тре́тіх"
    assert inflect("", "1002", "1003", fm("acc;m")) == "ти́сячу дві́ ти́сяча тре́тіх"

def test_1001_1002_1003():
    assert inflect("1001", "1002", "1003", fm("nom;m")) == "ти́сяча одна́ ці́ла ти́сяча дві́ ти́сяча тре́тіх"
    assert inflect("1001", "1002", "1003", fm("acc;m")) == "ти́сячу одну́ ці́лу ти́сячу дві́ ти́сяча тре́тіх"

def test_cases_sg():
    assert inflect("", "1", "3", fm("nom")) == "одна́ тре́тя" # частина
    assert inflect("", "1", "3", fm("gen")) == "одніє́ї тре́тьої" # частини
    assert inflect("", "1", "3", fm("dat")) == "одні́й тре́тій" # частині
    assert inflect("", "1", "3", fm("acc")) == "одну́ тре́тю" # частину
    assert inflect("", "1", "3", fm("inst")) == "одніє́ю тре́тьою" # частиною
    assert inflect("", "1", "3", fm("loc")) == "одні́й тре́тій" # частині
    assert inflect("", "1", "3", fm("voc")) == "одна́ тре́тя" # частино

def test_cases_pс():
    assert inflect("", "2", "3", fm("nom")) == "дві́ тре́тіх" # частини
    assert inflect("", "2", "3", fm("gen")) == "дво́х тре́тіх" # частин
    assert inflect("", "2", "3", fm("dat")) == "дво́м тре́тім" # частинам
    assert inflect("", "2", "3", fm("acc")) == "дві́ тре́тіх" # частини
    assert inflect("", "2", "3", fm("inst")) == "двома́ тре́тіми" # частинами
    assert inflect("", "2", "3", fm("loc")) == "дво́х тре́тіх" # частинах

def test_cases_pl():
    assert inflect("", "5", "3", fm("nom")) == "пʼя́ть тре́тіх" # частин
    assert inflect("", "5", "3", fm("gen")) == "пʼяти́ тре́тіх" # частин
    assert inflect("", "5", "3", fm("dat")) == "пʼяти́ тре́тім" # частинам
    assert inflect("", "5", "3", fm("acc")) == "пʼя́ть тре́тіх" # частин
    assert inflect("", "5", "3", fm("inst")) == "пʼятьма́ тре́тіми" # частинами
    assert inflect("", "5", "3", fm("loc")) == "пʼяти́ тре́тіх" # частинах

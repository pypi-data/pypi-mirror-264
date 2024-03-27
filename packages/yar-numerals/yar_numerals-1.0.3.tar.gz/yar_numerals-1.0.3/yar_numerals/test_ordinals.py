import pytest
from .ordinals import inflect
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
    assert inflect("0", fm("m")) == "нульови́й"
    assert inflect("0", fm("f")) == "нульова́"
    assert inflect("0", fm("n")) == "нульове́"
    assert inflect("0", fm("gen")) == "нульово́го"
    assert inflect("0", fm("gen;f")) == "нульово́ї"
    assert inflect("0", fm("acc;f;anim")) == "нульову́"
    assert inflect("0", fm("acc;f;inan")) == "нульову́"
    assert inflect("0", fm("loc;f")) == "нульові́й"


def test_lpad_0():
    assert inflect("00", {}) == "нульови́й"
    assert inflect("000000", {}) == "нульови́й"
    assert inflect("021", fm("m")) == "два́дцять пе́рший"
    assert inflect("0000000021", fm("m")) == "два́дцять пе́рший"


def test_21():
    assert inflect("21", fm("m")) == "два́дцять пе́рший"
    assert inflect("21", fm("f")) == "два́дцять пе́рша"
    assert inflect("21", fm("n")) == "два́дцять пе́рше"
    assert inflect("21", fm("gen")) == "два́дцять пе́ршого"
    assert inflect("21", fm("gen;f")) == "два́дцять пе́ршої"
    assert inflect("21", fm("acc;f;anim")) == "два́дцять пе́ршу"
    assert inflect("21", fm("acc;f;inan")) == "два́дцять пе́ршу"
    assert inflect("21", fm("loc;f")) == "два́дцять пе́ршій"


def test_713():
    assert inflect("713", fm("m")) == "сімсо́т трина́дцятий"
    assert inflect("713", fm("f")) == "сімсо́т трина́дцята"
    assert inflect("713", fm("n")) == "сімсо́т трина́дцяте"
    assert inflect("713", fm("gen")) == "сімсо́т трина́дцятого"
    assert inflect("713", fm("gen;f")) == "сімсо́т трина́дцятої"
    assert inflect("713", fm("acc;f;anim")) == "сімсо́т трина́дцяту"
    assert inflect("713", fm("acc;f;inan")) == "сімсо́т трина́дцяту"
    assert inflect("713", fm("loc;f")) == "сімсо́т трина́дцятій"


def test_1000():
    assert inflect("1000", fm("m")) == "ти́сячний"
    assert inflect("1000", fm("f")) == "ти́сячна"
    assert inflect("1000", fm("n")) == "ти́сячне"
    assert inflect("1000", fm("gen;m")) == "ти́сячного"
    assert inflect("1000", fm("gen;f")) == "ти́сячної"
    assert inflect("1000", fm("dat")) == "ти́сячному"
    assert inflect("1000", fm("acc;m;inan")) == "ти́сячний"
    assert inflect("1000", fm("acc;m;anim")) == "ти́сячного"
    assert inflect("1000", fm("acc;f;inan")) == "ти́сячну"
    assert inflect("1000", fm("acc;f;anim")) == "ти́сячну"
    assert inflect("1000", fm("acc;n;inan")) == "ти́сячне"
    assert inflect("1000", fm("acc;n;anim")) == "ти́сячне"
    assert inflect("1000", fm("acc;pl;inan")) == "ти́сячні"
    assert inflect("1000", fm("acc;pl;anim")) == "ти́сячних"
    assert inflect("1000", fm("loc;f")) == "ти́сячній"
    assert inflect("1000", fm("loc")) == "ти́сячному"
    assert inflect("1000", fm("inst")) == "ти́сячним"


def test_4486():
    assert inflect("4486", fm("m")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стий"
    assert inflect("4486", fm("f")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́ста"
    assert inflect("4486", fm("n")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сте"
    assert inflect("4486", fm("pl")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сті"

    assert inflect("4486", fm("gen;m")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стого"
    assert inflect("4486", fm("gen;f")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стої"
    assert inflect("4486", fm("gen;n")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стого"
    assert inflect("4486", fm("gen;pl")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стих"

    assert inflect("4486", fm("dat;m")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стому"
    assert inflect("4486", fm("dat;f")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стій"
    assert inflect("4486", fm("dat;n")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стому"
    assert inflect("4486", fm("dat;pl")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стим"

    assert inflect("4486", fm("acc;m;inan")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стий"
    assert inflect("4486", fm("acc;f;inan")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сту"
    assert inflect("4486", fm("acc;n;inan")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сте"
    assert inflect("4486", fm("acc;pl;inan")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сті"

    assert inflect("4486", fm("acc;m;anim")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стого"
    assert inflect("4486", fm("acc;f;anim")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сту"
    assert inflect("4486", fm("acc;n;anim")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сте"
    assert inflect("4486", fm("acc;pl;anim")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стих"

    assert inflect("4486", fm("inst;m")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стим"
    assert inflect("4486", fm("inst;f")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стою"
    assert inflect("4486", fm("inst;n")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стим"
    assert inflect("4486", fm("inst;pl")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стими"

    assert inflect("4486", fm("loc;m")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стому"
    assert inflect("4486", fm("loc;f")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стій"
    assert inflect("4486", fm("loc;n")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стому"
    assert inflect("4486", fm("loc;pl")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стих"

    assert inflect("4486", fm("voc;m")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́стий"
    assert inflect("4486", fm("voc;f")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́ста"
    assert inflect("4486", fm("voc;n")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сте"
    assert inflect("4486", fm("voc;pl")) == "чоти́ри ти́сячі чоти́риста вісімдеся́т шо́сті"


def test_525000():
    assert inflect("525000", fm("m")) == "пʼятисотдвадцятипʼятити́сячний"
    assert inflect("525000", fm("f")) == "пʼятисотдвадцятипʼятити́сячна"
    assert inflect("525000", fm("n")) == "пʼятисотдвадцятипʼятити́сячне"
    assert inflect("525000", fm("pl")) == "пʼятисотдвадцятипʼятити́сячні"

    assert inflect("525000", fm("gen;m")) == "пʼятисотдвадцятипʼятити́сячного"
    assert inflect("525000", fm("gen;f")) == "пʼятисотдвадцятипʼятити́сячної"
    assert inflect("525000", fm("gen;n")) == "пʼятисотдвадцятипʼятити́сячного"
    assert inflect("525000", fm("gen;pl")) == "пʼятисотдвадцятипʼятити́сячних"

    assert inflect("525000", fm("dat;m")) == "пʼятисотдвадцятипʼятити́сячному"
    assert inflect("525000", fm("dat;f")) == "пʼятисотдвадцятипʼятити́сячній"
    assert inflect("525000", fm("dat;n")) == "пʼятисотдвадцятипʼятити́сячному"
    assert inflect("525000", fm("dat;pl")) == "пʼятисотдвадцятипʼятити́сячним"

    assert inflect("525000", fm("acc;m;inan")) == "пʼятисотдвадцятипʼятити́сячний"
    assert inflect("525000", fm("acc;f;inan")) == "пʼятисотдвадцятипʼятити́сячну"
    assert inflect("525000", fm("acc;n;inan")) == "пʼятисотдвадцятипʼятити́сячне"
    assert inflect("525000", fm("acc;pl;inan")) == "пʼятисотдвадцятипʼятити́сячні"

    assert inflect("525000", fm("acc;m;anim")) == "пʼятисотдвадцятипʼятити́сячного"
    assert inflect("525000", fm("acc;f;anim")) == "пʼятисотдвадцятипʼятити́сячну"
    assert inflect("525000", fm("acc;n;anim")) == "пʼятисотдвадцятипʼятити́сячне"
    assert inflect("525000", fm("acc;pl;anim")) == "пʼятисотдвадцятипʼятити́сячних"

    assert inflect("525000", fm("inst;m")) == "пʼятисотдвадцятипʼятити́сячним"
    assert inflect("525000", fm("inst;f")) == "пʼятисотдвадцятипʼятити́сячною"
    assert inflect("525000", fm("inst;n")) == "пʼятисотдвадцятипʼятити́сячним"
    assert inflect("525000", fm("inst;pl")) == "пʼятисотдвадцятипʼятити́сячними"

    assert inflect("525000", fm("loc;m")) == "пʼятисотдвадцятипʼятити́сячному"
    assert inflect("525000", fm("loc;f")) == "пʼятисотдвадцятипʼятити́сячній"
    assert inflect("525000", fm("loc;n")) == "пʼятисотдвадцятипʼятити́сячному"
    assert inflect("525000", fm("loc;pl")) == "пʼятисотдвадцятипʼятити́сячних"

    assert inflect("525000", fm("voc;m")) == "пʼятисотдвадцятипʼятити́сячний"
    assert inflect("525000", fm("voc;f")) == "пʼятисотдвадцятипʼятити́сячна"
    assert inflect("525000", fm("voc;n")) == "пʼятисотдвадцятипʼятити́сячне"
    assert inflect("525000", fm("voc;pl")) == "пʼятисотдвадцятипʼятити́сячні"


def test_gender_with_plural():
    assert inflect("525000", fm("m;pl")) == "пʼятисотдвадцятипʼятити́сячні"
    assert inflect("525000", fm("gen;m;pl")) == "пʼятисотдвадцятипʼятити́сячних"
    assert inflect("525000", fm("dat;f;pl")) == "пʼятисотдвадцятипʼятити́сячним"
    assert inflect("525000", fm("loc;f;pl;anim")) == "пʼятисотдвадцятипʼятити́сячних"


def test_pravopys_p38():
    """§ 38 Складні числівники"""

    assert inflect("900", fm("m"), False) == "девʼятисо́тий"
    assert inflect("300", fm("m"), False) == "трьохсо́тий"
    assert inflect("2000", fm("m"), False) == "двохти́сячний"
    assert inflect("10000", fm("m"), False) == "десятити́сячний"
    assert inflect("4000000", fm("m"), False) == "чотирьохмільйо́нний"
    assert inflect("7000000000", fm("m"), False) == "семимілья́рдний"
    assert inflect("3000000000", fm("m"), False) == "трьохмілья́рдний"
    assert inflect("65000000", fm("m"), False) == "шістдесятипʼятимільйо́нний"
    assert inflect("1003000", fm("m"), False) == "мільйо́н трьохти́сячний"
    assert inflect("1004000000", fm("m"), False) == "мілья́рд чотирьохмільйо́нний"
    assert inflect("1988", fm("m"), False) == "ти́сяча девʼятсо́т вісімдеся́т во́сьмий"


def test_pravopys_p38_error():
    # There is an error in Правопис which led to incorrect example being printed
    assert inflect("530000", fm("m"), False) != "пʼятсоттридцятити́сячний"
    assert inflect("50000000", fm("m"), False) != "пʼятдесятимільйо́нний"


def test_pravopys_p38_corrected():
    assert inflect("530000", fm("m"), False) == "пʼятисоттридцятити́сячний"
    assert inflect("50000000", fm("m"), False) == "пʼятидесятимільйо́нний"


def test_pravopys_p106():
    """§ 106 Відмінювання порядкових числівників"""

    assert inflect("1", fm("m"), False) == "пе́рший"
    assert inflect("1", fm("f"), False) == "пе́рша"
    assert inflect("1", fm("n"), False) == "пе́рше"
    assert inflect("2", fm("m"), False) == "дру́гий"
    assert inflect("4", fm("m"), False) == "четве́ртий"
    assert inflect("5", fm("m"), False) == "пʼя́тий"
    assert inflect("6", fm("m"), False) == "шо́стий"
    assert inflect("7", fm("m"), False) == "сьо́мий"
    assert inflect("8", fm("m"), False) == "во́сьмий"
    assert inflect("9", fm("m"), False) == "девʼя́тий"
    assert inflect("10", fm("m"), False) == "деся́тий"
    assert inflect("11", fm("m"), False) == "одина́дцятий"
    assert inflect("12", fm("m"), False) == "двана́дцятий"
    assert inflect("20", fm("m"), False) == "двадця́тий"
    assert inflect("30", fm("m"), False) == "тридця́тий"
    assert inflect("40", fm("m"), False) == "сороко́вий"
    assert inflect("50", fm("m"), False) == "пʼятдеся́тий"
    assert inflect("60", fm("m"), False) == "шістдеся́тий"
    assert inflect("70", fm("m"), False) == "сімдеся́тий"
    assert inflect("80", fm("m"), False) == "вісімдеся́тий"
    assert inflect("90", fm("m"), False) == "девʼяно́стий"
    assert inflect("100", fm("m"), False) == "со́тий"
    assert inflect("200", fm("m"), False) == "двохсо́тий"
    assert inflect("300", fm("m"), False) == "трьохсо́тий"
    assert inflect("400", fm("m"), False) == "чотирьохсо́тий"
    assert inflect("500", fm("m"), False) == "пʼятисо́тий"
    assert inflect("1000", fm("m"), False) == "ти́сячний"
    assert inflect("2000", fm("m"), False) == "двохти́сячний"
    assert inflect("3000", fm("m"), False) == "трьохти́сячний"
    assert inflect("4000", fm("m"), False) == "чотирьохти́сячний"
    assert inflect("5000", fm("m"), False) == "пʼятити́сячний"
    assert inflect("1000000", fm("m"), False) == "мільйо́нний"
    assert inflect("2000000", fm("m"), False) == "двохмільйо́нний"
    assert inflect("3000000", fm("m"), False) == "трьохмільйо́нний"
    assert inflect("4000000", fm("m"), False) == "чотирьохмільйо́нний"
    assert inflect("5000000", fm("m"), False) == "пʼятимільйо́нний"
    assert inflect("3", fm("m"), False) == "тре́тій"
    assert inflect("3", fm("f"), False) == "тре́тя"
    assert inflect("3", fm("n"), False) == "тре́тє"
    assert inflect("88", fm("m"), False) == "вісімдеся́т во́сьмий"
    assert inflect("88", fm("gen;m"), False) == "вісімдеся́т во́сьмого"
    assert inflect("1991", fm("gen;m"), False) == "ти́сяча девʼятсо́т девʼяно́сто пе́ршого"
    assert inflect("1789", fm("loc;m"), False) == "ти́сяча сімсо́т вісімдеся́т девʼя́тому"
    assert inflect("2018", fm("dat;m"), False) == "дві́ ти́сячі вісімна́дцятому"


def test_range_fallback():
    assert inflect("999999999999999999999999999", fm("m")) == "девʼятсо́т девʼяно́сто де́вʼять септильйо́нів девʼятсо́т девʼяно́сто де́вʼять секстильйо́нів девʼятсо́т девʼяно́сто де́вʼять квінтильйо́нів девʼятсо́т девʼяно́сто де́вʼять квадрильйо́нів девʼятсо́т девʼяно́сто де́вʼять трильйо́нів девʼятсо́т девʼяно́сто де́вʼять мілья́рдів девʼятсо́т девʼяно́сто де́вʼять мільйо́нів девʼятсо́т девʼяно́сто де́вʼять ти́сяч девʼятсо́т девʼяно́сто девʼя́тий"
    assert inflect("1000000000000000000000000000", fm("m")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль нульови́й"
    assert inflect("1000000000000000000000000001", fm("m")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль пе́рший"
    assert inflect("1234567890123456789012345678", fm("m")) == "оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м во́сьмий"
    assert inflect("999999999999999999999999999", fm("f")) == "девʼятсо́т девʼяно́сто де́вʼять септильйо́нів девʼятсо́т девʼяно́сто де́вʼять секстильйо́нів девʼятсо́т девʼяно́сто де́вʼять квінтильйо́нів девʼятсо́т девʼяно́сто де́вʼять квадрильйо́нів девʼятсо́т девʼяно́сто де́вʼять трильйо́нів девʼятсо́т девʼяно́сто де́вʼять мілья́рдів девʼятсо́т девʼяно́сто де́вʼять мільйо́нів девʼятсо́т девʼяно́сто де́вʼять ти́сяч девʼятсо́т девʼяно́сто девʼя́та"
    assert inflect("1000000000000000000000000000", fm("f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль нульова́"
    assert inflect("1000000000000000000000000001", fm("f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль пе́рша"
    assert inflect("1234567890123456789012345678", fm("f")) == "оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м ві́сім де́вʼять ну́ль оди́н два́ три́ чоти́ри пʼя́ть ші́сть сі́м во́сьма"
    assert inflect("1000000000000000000000000000", fm("gen;f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль нульово́ї"
    assert inflect("1000000000000000000000000001", fm("gen;f")) == "оди́н ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль ну́ль пе́ршої"


def test_strict_range():
    inflect("999999999999999999999999999", fm("m"), strict_range=True)
    with pytest.raises(RangeError):
        assert inflect("1000000000000000000000000000", fm("m"), strict_range=True)


def test_10000000000000000000000000():
    assert inflect("100000000000000000000000000", fm("m")) == "стасептильйо́нний"


def test_insert_ones():
    assert inflect("100", fm("m"), insert_ones=True) == "со́тий"
    assert inflect("101", fm("m"), insert_ones=True) == "сто́ пе́рший"
    assert inflect("1000", fm("m"), insert_ones=True) == "ти́сячний"
    assert inflect("1001", fm("m"), insert_ones=True) == "одна́ ти́сяча пе́рший"
    assert inflect("1000000", fm("m"), insert_ones=True) == "мільйо́нний"
    assert inflect("1000001", fm("m"), insert_ones=True) == "оди́н мільйо́н пе́рший"
    assert inflect("100", fm("m"), insert_ones=True) == "со́тий"
    assert inflect("101", fm("f"), insert_ones=True) == "сто́ пе́рша"
    assert inflect("1000", fm("f"), insert_ones=True) == "ти́сячна"
    assert inflect("1001", fm("f"), insert_ones=True) == "одна́ ти́сяча пе́рша"
    assert inflect("1000000", fm("f"), insert_ones=True) == "мільйо́нна"
    assert inflect("1000001", fm("f"), insert_ones=True) == "оди́н мільйо́н пе́рша"


# fmt: on

from .grapheme import remove_stress


def test_remove_stress():
    assert remove_stress("") == ""
    assert remove_stress("оди́н") == "один"
    assert remove_stress("оди́н мільйо́н") == "один мільйон"
    assert remove_stress("о́о́о́о́") == "оооо"
    assert remove_stress("один") == "один"

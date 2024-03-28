import pytest
from gepref_text.normalization import (
        LowerStep, UpperStep, TitleStep, UnidecodeStep
        )

@pytest.mark.parametrize("text", [
    "Sample Text",
    "UPPERCASE TEXT",
    "lowercase text"
    ])
def test_lower_step(text: str):
    norm_text = LowerStep()(text)
    assert norm_text == text.lower()

@pytest.mark.parametrize("text", [
    "Sample Text",
    "UPPERCASE TEXT",
    "lowercase text"
    ])
def test_upper_step(text: str):
    norm_text = UpperStep()(text)
    assert norm_text == text.upper()

@pytest.mark.parametrize("text", [
    "Sample Text",
    "UPPERCASE TEXT",
    "lowercase text"
    ])
def test_title_step(text: str):
    norm_text = TitleStep()(text)
    assert norm_text == text.title()

@pytest.mark.parametrize("text, norm", [
    ("Gabriel García Márquez", "Gabriel Garcia Marquez"),
    ("También está considerado", "Tambien esta considerado")
    ])
def test_title_step(text: str, norm: str):
    norm_text = UnidecodeStep()(text)
    assert norm_text == norm

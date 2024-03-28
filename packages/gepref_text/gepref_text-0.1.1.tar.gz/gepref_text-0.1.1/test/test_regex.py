import re
import pytest
from gepref_text.regex import (
        RegexRemovalStep, UrlRemovalStep, SpRemovalStep,
        NumRemovalStep, DupSpacesStep
        )

class TestRegexRemoval:
    @pytest.mark.parametrize("text, pattern, result", [
        ("The 333 text", " 3{3,3} ", "The text"),
        ("absolute absurd", "abs", " olute  urd"),
        ])
    def test_patterns(self, text: str, pattern: str, result: str):
        pat = re.compile(pattern)
        norm_text = RegexRemovalStep().set_pattern(pat)(text)
        assert norm_text == result

    @pytest.mark.parametrize("text, replace_str, result", [
        ("the 123 is awesome", "man", "the man is awesome"),
        ("this 12356 the best", "is", "this is the best")
        ])
    def test_replace(self, text: str, replace_str: str, result: str):
        pat = re.compile(r"\d+")
        norm_text = (
                RegexRemovalStep()
                .set_pattern(pat)
                .set_replace_str(replace_str)(text)
                )
        assert norm_text == result

@pytest.mark.parametrize("text, result", [
    ("find the data https://amazingurl.com here", "find the data   here"),
    ("the http://amazingurl.com", "the  "),
    ("http://thisisit.es", " ")
    ])
def test_url_removal(text: str, result: str):
    norm_text = UrlRemovalStep()(text)
    assert norm_text == result

@pytest.mark.parametrize("text, result", [
    ("t*h-e@ messag.,_e", "the message"),
    ("1!2@3#4$5%6^7&8*9(0)", "1234567890"),
    ])
def test_sp_removal(text: str, result: str):
    norm_text = SpRemovalStep().set_replace_str('')(text)
    assert norm_text == result

@pytest.mark.parametrize("text, result", [
    ("this1is2it", "this is it"),
    ("12345abcd67809", " abcd "),
    ])
def test_num_removal(text: str, result: str):
    norm_text = NumRemovalStep()(text)
    assert norm_text == result

@pytest.mark.parametrize("text, result", [
    ("hello    world", "hello world"),
    ("the\n test", "the test"),
    ])
def test_dupspaces_removal(text: str, result: str):
    norm_text = DupSpacesStep()(text)
    assert norm_text == result

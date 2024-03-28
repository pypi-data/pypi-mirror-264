import re
from abc import ABC, abstractmethod
from typing import Optional
from gepref_text.base import AbstractTextStep

class AbstractRegexSubStep(AbstractTextStep, ABC):
    """
    Interface that defines any regex substitution preprocessing step.
    The `get_pattern` method must be implemented.

    :param pattern: Regex pattern to match.
    :type pattern: re.Pattern
    :param replace_str: String to replace.
    :type replace_str: str
    """

    pattern: Optional[re.Pattern] = None
    replace_str: str = ' '

    def set_replace_str(self, replace_str: str) -> "AbstractRegexSubStep":
        """
        Setter for the `replace_str` parameter.

        :param replace_str: String to replace
        :type replace_str: str
        :returns: Instance of the step
        :rtype: AbstractRegexSubStep
        """
        self.replace_str = replace_str
        return self

    def set_pattern(self, pattern: re.Pattern) -> "AbstractRegexSubStep":
        """
        Setter for the `pattern` parameter.

        :param pattern: Regex pattern to match.
        :type pattern: re.Pattern
        :returns: Instance of the step
        :rtype: AbstractRegexSubStep
        """
        self.pattern = pattern
        return self

    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        if self.pattern is None:
            self.pattern = self.get_pattern()
        return re.sub(self.pattern, self.replace_str, data)

    @abstractmethod
    def get_pattern(self) -> re.Pattern:
        ...

class RegexRemovalStep(AbstractRegexSubStep):
    """
    Step to replace a given text using a regex pattern. You can specify

    :param pattern: Regex pattern to match.
    :type pattern: re.Pattern
    :param replace_str: String to replace.
    :type replace_str: str
    """
    def get_pattern(self) -> re.Pattern:
        return re.compile(r"")

class UrlRemovalStep(AbstractRegexSubStep):
    """
    Step to remove an http or https url from text.

    :param pattern: Regex pattern to match.
    :type pattern: re.Pattern
    :param replace_str: String to replace.
    :type replace_str: str
    """
    def get_pattern(self) -> re.Pattern:
        return re.compile(r"https?://[^\s]+")

class SpRemovalStep(AbstractRegexSubStep):
    """
    Step to remove special characters (not letters or numbers) from text.

    :param pattern: Regex pattern to match.
    :type pattern: re.Pattern
    :param replace_str: String to replace.
    :type replace_str: str
    """
    def get_pattern(self) -> re.Pattern:
        return re.compile(r"[^a-zA-Z0-9 ]")

class NumRemovalStep(AbstractRegexSubStep):
    """
    Step to remove numbers from text.

    :param pattern: Regex pattern to match.
    :type pattern: re.Pattern
    :param replace_str: String to replace.
    :type replace_str: str
    """
    def get_pattern(self) -> re.Pattern:
        return re.compile(r"\d+")

class DupSpacesStep(AbstractRegexSubStep):
    """
    Step to remove duplicated spaces.

    :param pattern: Regex pattern to match.
    :type pattern: re.Pattern
    :param replace_str: String to replace.
    :type replace_str: str
    """
    def get_pattern(self) -> re.Pattern:
        return re.compile(r"\s+")

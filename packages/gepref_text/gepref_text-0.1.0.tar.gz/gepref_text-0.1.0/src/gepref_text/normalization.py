from unidecode import unidecode
from gepref_text.base import AbstractTextStep

class LowerStep(AbstractTextStep):
    """
    Converts the text to lowercase.
    """

    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        return data.lower()

class UpperStep(AbstractTextStep):
    """
    Converts the text to uppercase.
    """

    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        return data.upper()

class TitleStep(AbstractTextStep):
    """
    Converts the text to title.
    """

    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        return data.title()

class UnidecodeStep(AbstractTextStep):
    """
    Performs unidecode text normalization.
    """

    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        return unidecode(data)

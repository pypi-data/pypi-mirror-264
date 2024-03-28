from abc import ABC
from gepref.preprocessor import GenericPreprocessor
from gepref.step import AbstractStep

class TextPreprocessor(GenericPreprocessor[str]):
    """
    Processes input text elements through several preprocessing steps

    :param steps: list of preprocessing steps
    :type steps: List[AbstractStep[str]]
    """

class AbstractTextStep(AbstractStep[str], ABC):
    """
    Interface that defines the behavior of a text preprocessing step.
    It requires to implement the `call` method.
    """
    ...

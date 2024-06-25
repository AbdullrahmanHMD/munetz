from dataclasses import dataclass
from enum import Enum

@dataclass
class SummaryLengthRange:
    minimum : float
    maximum : float


class GPTType(Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT4O = "gpt-4o"
    GPT4 = "gpt-4"


class SummarizationLengthEnum(Enum):
    SHORT = SummaryLengthRange(minimum=0.15, maximum=0.24)
    MEDIUM = SummaryLengthRange(minimum=0.25, maximum=0.34)
    LONG = SummaryLengthRange(minimum=0.35, maximum=0.44)


class SummarizationLengthFactory:
    @staticmethod
    def get_summarization_length(summarization_len : str) -> SummarizationLengthEnum:
        valid_len = ['long', 'medium', 'short']
        assert summarization_len.lower() in valid_len, ValueError(f'Summarization length: {summarization_len} is invalid. Should be in {valid_len}')

        if summarization_len.lower() == 'long':
            return SummarizationLengthEnum.LONG
        elif summarization_len.lower() == 'medium':
            return SummarizationLengthEnum.MEDIUM
        elif summarization_len.lower() == 'short':
            return SummarizationLengthEnum.SHORT


class GPTPersonas(Enum):
    SUMMARIZATION = """PERSONA: You are a comprehensive document summarizer. Your ONLY task is to read the
following documents and summarize them, keeping only the most important and relevant information.
Ensure that the summary is concise, coherent, and captures the key points from each document."""

    INFO_EXTRACTION = """TO BE ADDED"""


class GPTPrompts(Enum):
    SUMMARIZATION = """Summarize the following text, make sure to keep the most important and relevant information
in the text. Ensure the summary is concise. Lastly, keep the summary strictly between {} and {} words"""

    INFO_EXTRACTION = """TO BE ADDED"""

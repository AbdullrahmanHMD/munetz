from dataclasses import dataclass
from enum import Enum

@dataclass
class SummaryLimit:
    minimum : float
    maximum : float


class GPTType(Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT4O = "gpt-4o"
    GPT4 = "gpt-4"


class SummarizationLengthEnum(Enum):
    SHORT = SummaryLimit(minimum=0.15, maximum=0.24)
    MEDIUM = SummaryLimit(minimum=0.25, maximum=0.34)
    LONG = SummaryLimit(minimum=0.35, maximum=0.44)


class GPTPersonas(Enum):
    SUMMARIZATION = """PERSONA: You are a comprehensive document summarizer. Your ONLY task is to read the
following documents and summarize them, keeping only the most important and relevant information.
Ensure that the summary is concise, coherent, and captures the key points from each document."""

    INFO_EXTRACTION = """TO BE ADDED"""


class GPTPrompts(Enum):
    SUMMARIZATION = """Summarize the following text, make sure to keep the most important and relevant information
in the text. Ensure the summary is concise. Lastly, keep the summary strictly between {} and {} words"""

    INFO_EXTRACTION = """TO BE ADDED"""

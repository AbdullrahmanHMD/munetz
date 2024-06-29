from dataclasses import dataclass
from enum import Enum

@dataclass
class SummaryLengthRange:
    minimum : float
    maximum : float

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

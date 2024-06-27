from abc import ABC, abstractmethod
from models.document_summarization.chatgpt_based.utils.chatgpt_data_schemas import SummarizationLengthEnum


class SummarizationModel(ABC):

    @abstractmethod
    def summarize(self, document_content : str, summarization_len : SummarizationLengthEnum) -> str:
        pass

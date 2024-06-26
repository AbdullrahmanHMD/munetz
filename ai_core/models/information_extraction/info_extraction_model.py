from abc import ABC, abstractmethod
from models.document_summarization.chatgpt_based.utils.chatgpt_data_schemas import SummarizationLengthEnum


class InformationExtractionModel(ABC):

    @abstractmethod
    def extract_info(self, document_content : str, extraction_prompt : str) -> str:
        pass

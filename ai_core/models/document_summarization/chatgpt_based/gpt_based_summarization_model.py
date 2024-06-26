# Ensure the folder1 is in the sys.path
from pathlib import Path
from models.document_summarization.chatgpt_based.utils.chatgpt_data_schemas import SummarizationLengthEnum
from models.chatgpt_based_models_utils.shared_eums import GPTPrompts
from models.chatgpt_based_models_utils.chatgpt_based_model import ChatGPTBasedModel

class GPTSummarizationModel(ChatGPTBasedModel):

    DEFAULT_CONFIG_PATH = Path(__file__).parent / "gpt_config.yaml"


    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH):
        super().__init__(config_path=config_path,
                         prompt=GPTPrompts.SUMMARIZATION.value)


    def summarize(self, document_content : str, summarization_len : SummarizationLengthEnum) -> str:
        words_num_in_document = len(document_content.split())
        sum_len_lower_limit = int(summarization_len.value.minimum * words_num_in_document)
        sum_len_upper_limit = int(summarization_len.value.maximum * words_num_in_document)

        prompt = self.prompt.format(sum_len_lower_limit, sum_len_upper_limit) + '\n' + document_content
        return self.query_model(prompt=prompt)

# Ensure the folder1 is in the sys.path
from openai import OpenAI

from pathlib import Path
from models.document_summarization.summarization_model import SummarizationModel
from utils.config_reader import read_config
from models.document_summarization.chatgpt_based.utils.chatgpt_data_schemas import GPTType, SummarizationLengthEnum, GPTPersonas, GPTPrompts

class GPTSummarizationModel(SummarizationModel):

    DEFAULT_CONFIG_PATH = Path(__file__).parent / "gpt_config.yaml"

    def __init__(self, config_path : Path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = read_config(self.config_path)
        self.client  = OpenAI(api_key=self.config['api_key'])
        self.role = self.config['model_config']['role']

        self.persona = GPTPersonas.SUMMARIZATION.value
        self.gpt_type = GPTType.GPT3.value
        self.prompt = GPTPrompts.SUMMARIZATION.value


    def summarize(self, document_content : str, summarization_len : SummarizationLengthEnum) -> str:
        words_num_in_document = len(document_content.split())
        sum_len_lower_limit = int(summarization_len.value.minimum * words_num_in_document)
        sum_len_upper_limit = int(summarization_len.value.maximum * words_num_in_document)

        prompt = self.persona + '\n' + self.prompt.format(sum_len_lower_limit, sum_len_upper_limit) + '\n' + document_content

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": self.role,
                    "content": prompt,
                }
            ],
            model=self.gpt_type,
        )

        summarized_doc = chat_completion.choices[0].message.content
        return summarized_doc

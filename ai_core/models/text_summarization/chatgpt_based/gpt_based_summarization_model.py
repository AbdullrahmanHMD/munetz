# Ensure the folder1 is in the sys.path
import sys
import openai
from openai import OpenAI

from pathlib import Path

abs_path = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(abs_path))

from models.summarization_model import SummarizationModel
from utils.config_reader import read_config, read_pdf
from models.text_summarization.chatgpt_based.utils.chatgpt_enums import GPTType, SummarizationLengthEnum, GPTPersonas, GPTPrompts

class GPTSummarizationModel(SummarizationModel):

    DEFAULT_CONFIG_PATH = Path(__file__).parent / "gpt_config.yaml"


    def __init__(self, save_path : Path=None, config_path : Path=DEFAULT_CONFIG_PATH):
        super().__init__(save_path)

        self.config_path = config_path
        self.config = read_config(self.config_path)
        self.client  = OpenAI(api_key=self.config['api_key'])
        self.role = self.config['model_config']['role']

        self.persona = GPTPersonas.SUMMARIZATION.value
        self.gpt_type = GPTType.GPT3.value
        self.prompt = GPTPrompts.SUMMARIZATION.value


    def summarize(self, document_path : Path, save_output_as_pdf : bool, summarization_len : SummarizationLengthEnum) -> str:

        document_content = read_pdf(doc_path=document_path)

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

        if save_output_as_pdf:
            GPTSummarizationModel.save_summarization_as_pdf(summarization=summarized_doc, save_path=self.save_path)
            return "Document summarized"
        else:
            return summarized_doc

if __name__=="__main__":
    model = GPTSummarizationModel(save_path="sum_test.pdf")
    doc_path = Path(__file__).parent.parent / 'docs' / 'article_1.pdf'
    print(model.summarize(document_path=doc_path, save_output_as_pdf=True, summarization_len=SummarizationLengthEnum.MEDIUM))

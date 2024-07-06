from pathlib import Path
from models.chatgpt_based_models_utils.shared_eums import GPTPrompts
from models.chatgpt_based_models_utils.chatgpt_based_model import ChatGPTBasedModel

class GPTInformationExtractionModel(ChatGPTBasedModel):

    DEFAULT_CONFIG_PATH = Path(__file__).parent / "gpt_config.yaml"

    def __init__(self, config_path : Path = DEFAULT_CONFIG_PATH):
        super().__init__(config_path=config_path,
                         prompt=GPTPrompts.INFO_EXTRACTION.value)


    def extract_info(self, documents_content : str, info_to_extraction : str) -> str:
        prompt = self.persona.get_persona() + '\n' + self.prompt.format(info_to_extraction) + '\n' + documents_content
        return self.query_model(prompt=prompt)

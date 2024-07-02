from openai import OpenAI

from pathlib import Path
from utils.config_reader import read_config
from models.chatgpt_based_models_utils.persona import Persona

class ChatGPTBasedModel():

    def __init__(self, config_path : Path, prompt : str):
        self.config = read_config(config_path)
        self.client  = OpenAI(api_key=self.config['api_key'])

        self.persona_role = self.config['model_config']['persona_role']
        self.query_role = self.config['model_config']['query_role']
        self.gpt_type = self.config['model_config']['gpt_type']

        self.persona = Persona.from_config(config=self.config['persona_config'])
        self.prompt = prompt


    def initialize_persona(self):
        _ = self.client.chat.completions.create(
            messages=[
                {
                    "role": self.persona_role,
                    "content": self.persona.get_persona(),
                }
            ],
            model=self.gpt_type,
        )

    def query_model(self, prompt : str):

        self.initialize_persona()

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": self.query_role,
                    "content": prompt,
                }
            ],
            model=self.gpt_type,
        )
        return chat_completion.choices[0].message.content

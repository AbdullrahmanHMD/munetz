# Ensure the folder1 is in the sys.path
from openai import OpenAI

from pathlib import Path
from utils.config_reader import read_config
from models.chatgpt_based_models_utils.persona import Persona

class ChatGPTBasedModel():

    def __init__(self, config_path : Path, prompt : str):
        self.config = read_config(config_path)
        self.client  = OpenAI(api_key=self.config['api_key'])

        self.role = self.config['model_config']['role']
        self.gpt_type = self.config['model_config']['gpt_type']

        self.persona = Persona.from_config(config=self.config['persona_config'])
        self.prompt = prompt

        self.initialize_persona()

    def initialize_persona(self):
        _ = self.client.chat.completions.create(
            messages=[
                {
                    "role": self.role,
                    "content": self.persona.get_persona(),
                }
            ],
            model=self.gpt_type,
        )

    def query_model(self, prompt : str):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": self.role,
                    "content": prompt,
                }
            ],
            model=self.gpt_type,
        )
        return chat_completion.choices[0].message.content

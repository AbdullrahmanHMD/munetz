from pathlib import Path
from typing import Union

class Persona:

    def __init__(self, persona_path : Union[Path, str], persona_file_name : str):
        self.persona_path = Path(persona_path) / persona_file_name
        self.persona_content = Persona.load_persona(self.persona_path)

    @classmethod
    def from_config(cls, config: dict):
        return cls(**config)

    @staticmethod
    def load_persona(persona_path):
        with open(persona_path, 'r') as file:
            persona_content = ""
            for line in file.readlines():
                persona_content += line
        return persona_content

    def __repr__(self):
        return f"Persona({self.persona_path}):\\n{self.persona_content}"

    def get_persona(self):
        return self.persona_content

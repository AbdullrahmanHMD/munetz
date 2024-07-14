from openai import OpenAI
import openai
from pathlib import Path
from dataclasses import asdict
from utils.config_reader import read_config
from models.assistant_based_models_utils.data_schemas import AssistantConfig


class AssistantHandler:
    def __init__(self, api_key : str):
        self._client = OpenAI(api_key=api_key)

    @property
    def client(self):
        return self._client

    def load_assistant_from_config(self, config_path : Path) -> openai.types.beta.assistant.Assistant:
        config = read_config(config_path=config_path)
        return self.client.beta.assistants.retrieve(assistant_id=config['assistant_id'])

    def get_assistant_from_id(self, id : str) -> openai.types.beta.assistant.Assistant:
        return self.client.beta.assistants.retrieve(assistant_id=id)

    def delete_assistant(self, assistant : openai.types.beta.assistant.Assistant) -> None:
        self.client.beta.assistants.delete(assistant_id=assistant.id)

    def create_new_assistant(self, assistant_config : AssistantConfig):
        return self.client.beta.assistants.create(**asdict(assistant_config))

    def update_instruction(self, assistant_id : str, instructions : str):
        self.client.beta.assistants.update(assistant_id=assistant_id, instructions=instructions)

    def update_model(self, assistant_id : str, model : str):
        self.client.beta.assistants.update(assistant_id=assistant_id, model=model)

    def update_name(self, assistant_id : str, name : str):
        self.client.beta.assistants.update(assistant_id=assistant_id, name=name)

    def update_tools(self, assistant_id : str, tools : list):
        self.client.beta.assistants.update(assistant_id=assistant_id, tools=tools)


class ThreadHandler:
    def __init__(self, api_key : str):
        self._client = OpenAI(api_key=api_key)

    @property
    def client(self):
        return self._client

    def load_thread_from_config(self, config_path : Path) -> openai.types.beta.thread.Thread:
        config = read_config(config_path=config_path)
        return self.client.beta.threads.retrieve(thread_id=config['thread_id'])

    def get_thread_from_id(self, id : str) -> openai.types.beta.thread.Thread:
        return self.client.beta.threads.retrieve(thread_id=id)

    def delete_thread(self, id : str) -> None:
        self.client.beta.threads.delete(thread_id=id)

    def create_new_thread(self):
        return self.client.beta.threads.create()

import openai
from openai import OpenAI
from abc import ABC, abstractmethod

class AbstractAssistant(ABC):
    def __init__(self, assistant : openai.types.beta.assistant.Assistant,
                 thread : openai.types.beta.thread.Thread,
                 api_key : str):
        self._assistant = assistant
        self._thread = thread
        self._client = OpenAI(api_key=api_key)

    @property
    def assistant(self):
        return self._assistant

    @property
    def thread(self):
        return self._thread

    @property
    def client(self):
        return self._client

    @assistant.setter
    def assistant(self, assistant):
        self._assistant = assistant

    @thread.setter
    def thread(self, thread):
        self._thread = thread

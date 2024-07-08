from pathlib import Path
import pickle
from dataclasses import asdict
from models.chatbot.chatgpt_based.utils.data_schemas import ChatBotMessage


class ChatHistory():
    def __init__(self, history_depth : int, history_folder_path : Path, history_file_name : str):
        self.history_folder_path = Path(history_folder_path)
        self.history_file_name = history_file_name
        self.history_file_path = self.history_folder_path / self.history_file_name
        self.history_depth = history_depth
        try:
            self._history = self.load_history()
        except EOFError:
            self._history = []


    @classmethod
    def from_config(cls, config : dict):
        return cls(**config)


    def load_history(self) -> list:
        with open(self.history_file_path, 'rb') as file:
            history_list = pickle.load(file)[-self.history_depth:]
        return history_list


    def append_to_history(self, to_append : ChatBotMessage) -> list:
        self._history.append(asdict(to_append))
        self.save_history()
        self._history = self.load_history()
        return self._history


    def save_history(self) -> None:
        with open(self.history_file_path, 'wb') as file:
            pickle.dump(self._history, file)


    def clear_history(self) -> None:
        self._history = []
        self.save_history()

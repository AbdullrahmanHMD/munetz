from pathlib import Path


class ChatBotKnowledge:
    def __init__(self, knowledge_folder_path : Path, knowledge_files_to_use : list[str]):
        self.knowledge_folder_path = Path(knowledge_folder_path)
        self.knowledge_files_to_use = knowledge_files_to_use

    @classmethod
    def from_config(cls, config : dict):
        return cls(**config)

    def get_knowledge(self):
        full_paths = [self.knowledge_folder_path / path for path in self.knowledge_files_to_use]

        full_knowledge_str = ""
        for i, path in enumerate(full_paths):
            with open(path, 'r', encoding='utf-8') as file:
                full_knowledge_str += f"Knowledge file #{i}\n{file.read()}\n\n"

        return full_knowledge_str

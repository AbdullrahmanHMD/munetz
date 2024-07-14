import openai
from openai import OpenAI
from pathlib import Path
import yaml

ALLOWED_FILE_TYPES = ['.pdf', '.html', ".txt"]

class FileManager:
    def __init__(self, api_key : str):
        files_path = Path(__file__).resolve().parent / "files.yaml"
        if not files_path.exists():
            Path.touch(files_path)
        self.files_path = files_path
        self._client = OpenAI(api_key=api_key)

    @property
    def client(self):
        return self._client

    def craete_file(self, file_path : Path, purpose : str ="assistants") -> openai.types.file_object.FileObject:
        file = self.client.files.create(file=open(file_path, "rb"), purpose=purpose)
        self._add_file_id(file.id)
        return file

    def delete_file(self, file_id : str) -> None:
        self.client.files.delete(file_id=file_id)
        self._delete_file_id(file_id=file_id)

    def get_file(self, file_id : str) -> openai.types.file_object.FileObject:
        return self.client.files.retrieve(file_id=file_id)

    def create_files(self, files_to_add : list[Path]) -> list[openai.types.file_object.FileObject]:
        files = []
        for file in files_to_add:
            files.append(self.craete_file(file))
        return files

    def delete_files(self, files_to_delete : list[str]):
        for file in files_to_delete:
            self.delete_file(file)

    def create_files_in_folder(self, folder_path : Path) -> list[openai.types.file_object.FileObject]:
        folder = Path(folder_path)
        file_paths = [file for file in folder.iterdir() if file.is_file() and file.suffix in ALLOWED_FILE_TYPES]
        files = self.create_files(files_to_add=file_paths)
        return files

    def delete_all_files(self):
        with open(self.files_path, 'r') as file:
            config = yaml.safe_load(file)

        if config is None or 'files' not in config or not isinstance(config['files'], list):
            return

        for file_id in config['files']:
            self.delete_file(file_id)

    def get_all_files(self) -> list[openai.types.file_object.FileObject]:
        with open(self.files_path, 'r') as file:
            config = yaml.safe_load(file)

        files = []

        if config is None or 'files' not in config or not isinstance(config['files'], list):
            return files

        for file_id in config['files']:
            files.append(self.get_file(file_id=file_id))

        return files

    def _add_file_id(self, file_id: str) -> None:

        with open(self.files_path, 'r') as file:
            config = yaml.safe_load(file)

        if config is None:
            config = {"files" : []}

        if not isinstance(config['files'], list) or 'files' not in config:
            config['files'] = []

        config['files'].append(file_id)
        config['files'] = list(set(config['files']))

        with open(self.files_path, 'w') as file:
            yaml.safe_dump(config, file, default_flow_style=False)

    def _delete_file_id(self, file_id : str) -> None:
        with open(self.files_path, 'r') as file:
            config = yaml.safe_load(file)

        if config is None or 'files' not in config or not isinstance(config['files'], list):
            return

        if file_id in config['files']:
            config['files'].remove(file_id)

            with open(self.files_path, 'w') as file:
                yaml.safe_dump(config, file, default_flow_style=False)

# new_file = "file_2.pdf"

# # delete_file(files_path, new_file)
# # add_file(files_path, new_file)

# file_id ="file-w1QGJ9vWzYDvOKjdjINYz2gt"
# api_key = "sk-proj-wmExG8KsPuL9RgAkUJuuT3BlbkFJbGWYOUBu7SzkI9LHdEwF"

# folder_path = Path(__file__).resolve().parent
# file_manager = FileManager(api_key=api_key)
# file_manager.delete_all_files()

# file_manager = FileManager(api_key=api_key)
# # file_manager.delete_file(file_id=file_id)
# # file_manager.delete_file(new_file)
# # print(type(file_manager.get_file(file_id=file_id)))

# file_paths = [Path(__file__).resolve().parent / "munich.pdf", Path(__file__).resolve().parent / "article_1.pdf"]

# # print(file_manager.craete_file(file_path=file_path))
# # file_manager.delete_all_files()

# file_manager.delete_all_files()

# client = OpenAI(api_key=api_key)
# print(client.files.retrieve(file_id=file_id))

import openai
from pathlib import Path
from models.information_extraction.assistant_based.utils.file_manager import FileManager
from models.assistant_based_models_utils.abstract_assistant_model import AbstractAssistant


class InfoExtractionAssistant(AbstractAssistant):
    def __init__(self, assistant : openai.types.beta.assistant.Assistant,
                 thread : openai.types.beta.thread.Thread,
                 api_key : str):
        super().__init__(assistant=assistant, thread=thread, api_key=api_key)
        self.folder_path = Path(__file__).resolve().parent
        self.file_manager = FileManager(api_key=api_key)

    def query_model(self, message : str, files_to_create : list[Path], role : str = "user") -> None:

        files = self.file_manager.create_files(files_to_add=files_to_create)
        attachments = [{"file_id" : file.id, "tools" : [{"type" : "file_search"}]} for file in files]

        message = self.client.beta.threads.messages.create(thread_id=self.thread.id, role=role, content=message, attachments=attachments)

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id, assistant_id=self.assistant.id
        )

        messages = list(self.client.beta.threads.messages.list(thread_id=self.thread.id, run_id=run.id))
        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []

        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        self.file_manager.delete_all_files()
        return message_content.value

    def __repr__(self):
        return f"InfoExtractionAssistant(assistant={self.assistant}, thread={self.thread}, client={self.client})"

import openai
from models.assistant_based_models_utils.abstract_assistant_model import AbstractAssistant

class ChatBotAssistant(AbstractAssistant):
    def __init__(self, assistant : openai.types.beta.assistant.Assistant,
                 thread : openai.types.beta.thread.Thread,
                 api_key : str):
        super().__init__(assistant=assistant, thread=thread, api_key=api_key)


    def query_model(self, message : str, role : str = "user"):
        message = self.client.beta.threads.messages.create(thread_id=self.thread.id, role=role, content=message)
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

        return message_content.value

    def __repr__(self):
        return f"ChatBotAssistant(assistant={self.assistant}, thread={self.thread}, client={self.client})"

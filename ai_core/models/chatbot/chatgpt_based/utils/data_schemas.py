from dataclasses import dataclass


@dataclass
class ChatBotMessage:
    role : str
    message_content : str

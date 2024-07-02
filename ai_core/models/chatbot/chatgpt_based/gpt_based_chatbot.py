from pathlib import Path
from models.chatgpt_based_models_utils.shared_eums import GPTPrompts
from models.chatgpt_based_models_utils.chatgpt_based_model import ChatGPTBasedModel
from models.chatbot.chatgpt_based.utils.chat_history import ChatHistory
from models.chatbot.chatgpt_based.utils.data_schemas import ChatBotMessage
from models.chatbot.chatgpt_based.utils.chatbot_knowledge import ChatBotKnowledge

class GPTChatBotModel(ChatGPTBasedModel):

    DEFAULT_CONFIG_PATH = Path(__file__).parent / "gpt_config.yaml"

    def __init__(self, config_path : Path = DEFAULT_CONFIG_PATH):
        super().__init__(config_path=config_path,
                         prompt=GPTPrompts.CHATBOT.value)

        self.history = ChatHistory.from_config(self.config['history_config'])
        self.knowledge = ChatBotKnowledge.from_config(self.config['knowledge_config'])

    def query_chat(self, user_message : str, load_history : bool) -> str:
        history = None
        if load_history:
            history = self.history.load_history()
        else:
            history = "EMPTY_HISTORY"

        prompt = self.prompt.format(self.knowledge.get_knowledge(), user_message, history)
        model_response = self.query_model(prompt=prompt)

        self.history.append_to_history(ChatBotMessage(role="user", message_content=user_message))
        self.history.append_to_history(ChatBotMessage(role="assistance", message_content=model_response))
        return model_response

from pathlib import Path
import argparse
import sys
import yaml
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.pdf_creator.data_schemas import *
from models.chatbot.assistant_based.assistant_based_chatbot import ChatBotAssistant
from models.assistant_based_models_utils.handlers import AssistantHandler, ThreadHandler
from models.assistant_based_models_utils.enums import AssistantIDs
from utils.config_reader import read_config
from models.chatgpt_based_models_utils.persona import Persona

def main():

    parser = argparse.ArgumentParser(description="A script for running the chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt of the user to relay to the chatbot")
    parser.add_argument("-t", "--do_not_use_history", action="store_false", help="A boolean that specifies whether to use the history or not")
    parser.add_argument("-c", "--clear_history", action="store_true", help="A boolean that specifies whether to clear the history or not")

    args = parser.parse_args()

    config_path = Path(__file__).resolve().parent / "script_config.yaml"
    script_config = read_config(config_path)

    api_key = script_config['api_key']

    persona = Persona.from_config(script_config['persona_config'])

    assistant_handler = AssistantHandler(api_key=api_key)
    thread_handler = ThreadHandler(api_key=api_key)

    assistant = assistant_handler.get_assistant_from_id(id=AssistantIDs.CHATBOT.value)
    assistant_handler.update_instruction(assistant_id=assistant.id, instructions=str(persona))

    if "thread_id" not in script_config.keys():
        thread = thread_handler.create_new_thread()
        script_config['thread_id'] = thread.id

        with open(config_path, 'w') as file:
            yaml.safe_dump(script_config, file)
    else:
        if args.clear_history:
            thread_handler.delete_thread(id=script_config['thread_id'])
            thread = thread_handler.create_new_thread()
            script_config['thread_id'] = thread.id

            with open(config_path, 'w') as file:
                yaml.safe_dump(script_config, file)
        else:
            thread = thread_handler.load_thread_from_config(config_path=config_path)

    # Querying the chatbot
    chatbot = ChatBotAssistant(assistant=assistant, thread=thread, api_key=api_key)
    print(chatbot.query_model(message=args.user_prompt))


if __name__=="__main__":
    main()

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config_reader import read_config, read_pdf
from utils.pdf_creator.data_schemas import *
from models.chatbot.chatgpt_based.gpt_based_chatbot import GPTChatBotModel


def main():
    # Setting up the script's arguments:
    script_defaults_config_path = Path(__file__).resolve().parent / 'script_defaults.yaml'
    script_defaults = read_config(script_defaults_config_path)

    parser = argparse.ArgumentParser(description="A script for running the chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt of the user to relay to the chatbot")
    parser.add_argument("-t", "--use_history", action="store_true", help="A boolean that specifies whether to the history or not")

    args = parser.parse_args()
    print(args.use_history)
    # Querying the chatbot
    chatbot = GPTChatBotModel()
    chatbot_response = chatbot.query_chat(user_message=args.user_prompt, load_history=args.use_history)
    print(chatbot_response)

if __name__=="__main__":
    main()

from pathlib import Path
import argparse
import sys
import yaml
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.pdf_creator.data_schemas import *
from models.assistant_based_models_utils.handlers import AssistantHandler, ThreadHandler
from models.assistant_based_models_utils.enums import AssistantIDs
from utils.config_reader import read_config
from models.chatgpt_based_models_utils.persona import Persona
from models.information_extraction.assistant_based.assistant_based_info_extraction import InfoExtractionAssistant
from models.chatgpt_based_models_utils.shared_eums import GPTPrompts

def parse_extracted_info(info : str, info_list : list) -> dict:
    info_dict = {}
    for line in info.split('\n'):
        colon_idx = line.find(':')
        if colon_idx != -1:
            key, val = line[:colon_idx].strip(), line[colon_idx + 1:].strip()
            if key in info_list:
                info_dict[key] = val
    return info_dict


def validate_extracted_info(extracted_info : dict, information_to_extract : list) -> bool:
    for info in information_to_extract :
        if info not in list(extracted_info.keys()):
            return False
    return True

def main():

    config_path = Path(__file__).resolve().parent / 'script_config.yaml'
    script_config = read_config(config_path)

    parser = argparse.ArgumentParser(description="A script for extracting information from PDF documents")
    parser.add_argument('doc_names', metavar='N', type=str, nargs='+', help='an integer for the accumulator')
    parser.add_argument("html_name", type=str, help="The name of the HTML file of the webpage to extract information from.")
    parser.add_argument("-p", "--doc_path", type=str, default=script_config['doc_default_path'],
                        help="The path of the folder of the document to extract information from.")

    args = parser.parse_args()


    api_key = script_config['api_key']
    info_to_extract = script_config['info_to_extract']

    doc_folder_path, docs_names = args.doc_path, args.doc_names
    file_paths = [Path(doc_folder_path) / path for path in [*docs_names, args.html_name]]

    persona = Persona.from_config(script_config['persona_config'])

    assistant_handler = AssistantHandler(api_key=api_key)
    thread_handler = ThreadHandler(api_key=api_key)

    assistant = assistant_handler.get_assistant_from_id(id=AssistantIDs.INFO_EXTRACTION.value)
    assistant_handler.update_instruction(assistant_id=assistant.id, instructions=str(persona))

    thread = thread_handler.create_new_thread()

    info_extractor = InfoExtractionAssistant(assistant=assistant, thread=thread, api_key=api_key)

    message = GPTPrompts.INFO_EXTRACTION.value.format(info_to_extract)
    extracted_info = info_extractor.query_model(message=message, files_to_create=file_paths)
    parsed_extracted_info = parse_extracted_info(info=extracted_info, info_list=info_to_extract)
    print(json.dumps(parsed_extracted_info))

    thread_handler.delete_thread(id=thread.id)

if __name__=="__main__":
    main()

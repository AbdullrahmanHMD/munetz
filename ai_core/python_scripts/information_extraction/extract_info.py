from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config_reader import read_config, read_pdf
from utils.pdf_creator.data_schemas import *
from models.information_extraction.chatgpt_based.gpt_based_info_extraction_model import GPTInformationExtractionModel


def parse_extracted_info(info : str, info_list : list) -> dict:
    info_dict = {}
    for line in info.split('\n'):
        colon_idx = line.find(':')
        if colon_idx != -1:
            key, val = line[:colon_idx].strip(), line[colon_idx + 1:].strip()
            if key in info_list:
                info_dict[key] = val
    return info_dict

def main():
    # Setting up the script's arguments:
    script_defaults_config_path = Path(__file__).resolve().parent / 'script_defaults.yaml'
    script_defaults = read_config(script_defaults_config_path)

    parser = argparse.ArgumentParser(description="A script for summarizing PDF documents")
    parser.add_argument("doc_name", type=str, help="The name of the document to extract information from.")
    parser.add_argument("html_file", type=str, help="The HTML file of the webpage to extract information from.")
    parser.add_argument("-p", "--doc_path", type=str, default=script_defaults['doc_default_path'],
                        help="The path of the folder of the document to extract information from.")

    args = parser.parse_args()

    info_to_extract = script_defaults['info_to_extract']

    # Loading the PDF document to extract information from:
    doc_folder_path, doc_name = args.doc_path, args.doc_name
    doc_path = Path(doc_folder_path) / doc_name
    document_content = read_pdf(doc_path=doc_path)
    all_content = f"PDF content:\n {document_content}\n\nHTML content:\n {args.html_file}"

    # Loading the information extraction model:
    information_extraction_model = GPTInformationExtractionModel()
    extracted_info = information_extraction_model.extract_info(document_content=all_content, info_to_extraction=info_to_extract)
    print(parse_extracted_info(info=extracted_info, info_list=info_to_extract))


if __name__=="__main__":
    main()

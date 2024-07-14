from pathlib import Path
import argparse
import sys
import json

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config_reader import read_config, read_pdf, read_pdfs, read_and_parse_html
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


def validate_extracted_info(extracted_info : dict, information_to_extract : list) -> bool:
    for info in information_to_extract :
        if info not in list(extracted_info.keys()):
            return False
    return True


def main():
    # Setting up the script's arguments:
    script_defaults_config_path = Path(__file__).resolve().parent / 'script_defaults.yaml'
    script_defaults = read_config(script_defaults_config_path)

    parser = argparse.ArgumentParser(description="A script for extracting information from PDF documents")
    parser.add_argument('doc_names', metavar='N', type=str, nargs='+', help='an integer for the accumulator')
    parser.add_argument("html_name", type=str, help="The name of the HTML file of the webpage to extract information from.")
    parser.add_argument("-p", "--doc_path", type=str, default=script_defaults['doc_default_path'],
                        help="The path of the folder of the document to extract information from.")

    args = parser.parse_args()

    info_to_extract = script_defaults['info_to_extract']

    # Loading the PDF document and the HTML file to extract information from:
    doc_folder_path, docs_names = args.doc_path, args.doc_names
    docs_paths = [Path(doc_folder_path) / path for path in docs_names]
    documents_content = read_pdfs(doc_paths=docs_paths)

    html_name, html_folder_path = args.html_name, args.doc_path
    html_path = Path(html_folder_path) / html_name

    html_content = read_and_parse_html(html_path=html_path)

    # Loading the information extraction model:
    information_extraction_model = GPTInformationExtractionModel()
    num_retries = script_defaults['num_to_retry_prompt']

    documents_content.append(html_content)
    extracted_info_dict = dict(zip(info_to_extract, [[] for _ in range(len(info_to_extract))]))
    response_is_valid = [False]

    for document_content in documents_content:
        for _ in range(num_retries):
            extracted_info = information_extraction_model.extract_info(documents_content=document_content, info_to_extraction=info_to_extract)
            parsed_extracted_info = parse_extracted_info(info=extracted_info, info_list=info_to_extract)
            if validate_extracted_info(extracted_info=parsed_extracted_info, information_to_extract=info_to_extract):
                for key, val in parsed_extracted_info.items():
                    if val.lower().lstrip().rstrip() != "not found":
                        extracted_info_dict[key].append(val)
                response_is_valid.append(True)
                continue

    if sum(response_is_valid) == 0:
        print(json.dumps({"error":"Could not extract information, please try again later"}))
    else:
        for key, val in extracted_info_dict.items():
            extracted_info_dict[key] = list(set(val))
        print(json.dumps(extracted_info_dict))


if __name__=="__main__":
    main()

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config_reader import read_config, read_pdf
from utils.pdf_creator.data_schemas import *
from models.information_extraction.chatgpt_based.gpt_based_info_extraction_model import GPTInformationExtractionModel


def parse_extraced_info(info : str) -> dict:
    extracted_data = {}

    # Find the starting point
    start_marker = 'EXTRACTION_TEMPLATE:'
    start_index = info.find(start_marker)

    # Ensure the marker is found
    if start_index != -1:
        # Extract substring starting from the marker
        substring = info[start_index + len(start_marker):]

        # Split substring into lines
        lines = substring.splitlines()

        # Process each line to form key-value pairs until a blank line or end of input
        for line in lines:
            line = line.strip()
            if not line:
                break  # Stop processing on encountering a blank line

            # Split key-value pair by colon
            key, value = line.split(':', 1)

            # Strip whitespace from key and value
            key = key.strip()
            value = value.strip()

            # Store in dictionary
            extracted_data[key] = value
    return extracted_data # TODO: While parsing the output, keep only the information keys you already have.


def main():
    # Setting up the script's arguments:
    script_defaults_config_path = Path(__file__).resolve().parent / 'script_defaults.yaml'
    script_defaults = read_config(script_defaults_config_path)

    parser = argparse.ArgumentParser(description="A script for summarizing PDF documents")

    parser.add_argument("doc_name", type=str, help="The name of the document to extract information from.")
    # parser.add_argument("html_file", type=str, help="The HTML file of the webpage to extract information from.")
    parser.add_argument("-i", "--info_to_extract", type=str, default=script_defaults['info_to_extract'],
                        help="The information to extract from the given document")
    parser.add_argument("-p", "--doc_path", type=str, default=script_defaults['doc_default_path'],
                        help="The path of the folder of the document to extract information from.")

    args = parser.parse_args()

    # Loading the PDF document to extract information from:
    doc_folder_path, doc_name = args.doc_path, args.doc_name
    doc_path = Path(doc_folder_path) / doc_name
    document_content = read_pdf(doc_path=doc_path)

    # Loading the information extraction model:
    information_extraction_model = GPTInformationExtractionModel()
    extracted_info = information_extraction_model.extract_info(document_content=document_content, info_to_extraction=args.info_to_extract.split(","))
    print(extracted_info)
    # print(parse_extraced_info(extracted_info))

if __name__=="__main__":
    main()

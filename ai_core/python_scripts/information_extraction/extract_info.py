from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config_reader import read_config, read_pdf
from utils.pdf_creator.data_schemas import *
from models.information_extraction.chatgpt_based.gpt_based_info_extraction_model import GPTInformationExtractionModel


def main():
    # Setting up the script's arguments:
    script_defaults_config_path = Path(__file__).resolve().parent / 'script_defaults.yaml'
    script_defaults = read_config(script_defaults_config_path)

    parser = argparse.ArgumentParser(description="A script for summarizing PDF documents")

    parser.add_argument("doc_name", type=str, help="The name of the document to extract information from.")
    parser.add_argument("info_to_extract", type=str,
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
    extracted_info = information_extraction_model.extract_info(document_content=document_content, extraction_prompt=args.info_to_extract)
    print(extracted_info)

if __name__=="__main__":
    main()

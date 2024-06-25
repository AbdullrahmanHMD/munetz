from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config_reader import read_config, read_pdf
from utils.pdf_creator.pdf_creator import PDFCreator
from utils.pdf_creator.data_schemas import *
from models.document_summarization.chatgpt_based.gpt_based_summarization_model import GPTSummarizationModel
from models.document_summarization.chatgpt_based.utils.chatgpt_data_schemas import SummarizationLengthFactory


def main():
    # Setting up the script's arguments:
    script_defaults_config_path = Path(__file__).resolve().parent / 'script_defaults.yaml'
    script_defaults = read_config(script_defaults_config_path)

    parser = argparse.ArgumentParser(description="A script for summarizing PDF documents")

    parser.add_argument("doc_name", type=str, help="The name of the document to summarize.")
    parser.add_argument("-p", "--doc_path", type=str, default=script_defaults['doc_default_path'],
                        help="The path of the folder of the document to summarize.")
    parser.add_argument("-s", "--save_path", type=str, default=script_defaults['doc_save_path'],
                        help="The path where the summarized document will be saved.")
    parser.add_argument("-l", "--sum_len", type=str, default=script_defaults['summarization_len'],
                        help=" The length of the summarization.")
    parser.add_argument("-f", "--save_pdf", type=bool, default=script_defaults['save_as_pdf'],
                        help="Whether to save the document as PDF or return it as text.")

    args = parser.parse_args()

    # Loading the PDF document to summarize:
    doc_folder_path, doc_name = args.doc_path, args.doc_name
    doc_path = Path(doc_folder_path) / doc_name
    document_content = read_pdf(doc_path=doc_path)

    # Loading the summarization model:
    summarization_model = GPTSummarizationModel()

    summarization_len = SummarizationLengthFactory.get_summarization_length(args.sum_len)
    document_summary = summarization_model.summarize(document_content=document_content, summarization_len=summarization_len)

    if args.save_pdf:
        original_doc_name = doc_name.split('.')[0]
        title = f"Summarization of {original_doc_name}"
        department = "Culture"
        contact_info = "example@domain.com"

        document_size = DocumentSizeEnum.A4
        document_style = DocumentStyleEnum.LINEAR
        text_margin = 72

        title_section = DocumentSection(content=title, font=FontEnum.HELV, font_size=FontSizeEnum.TITLE, text_color=(0, 0, 0))
        department_name_section = DocumentSection(content=f"Department: {department}", font=FontEnum.HELV, font_size=FontSizeEnum.SUBHEADING, text_color=(0.2, 0.2, 0.2))
        contact_info_section = DocumentSection(content=f"Contact Info: {contact_info}", font=FontEnum.HELV, font_size=FontSizeEnum.SUBHEADING, text_color=(0.2, 0.2, 0.2))
        content_section = DocumentSection(content=document_summary, font=FontEnum.HELV, font_size=FontSizeEnum.BODY_MEDIUM, text_color=(0, 0, 0))

        sections = [title_section, department_name_section, contact_info_section, content_section]

        summarized_doc_name = f"{original_doc_name}_summarized.pdf"
        doc_save_path = Path(args.save_path) / summarized_doc_name

        pdf_creator = PDFCreator(document_size=document_size, sections=sections, document_style=document_style, text_margin=text_margin)
        pdf_creator.create_pdf_doc(doc_save_path)
        print("document summarized")
    else:
        print(document_summary)


if __name__=="__main__":
    main()

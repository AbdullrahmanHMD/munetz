from pathlib import Path

from utils.config_reader import read_config, read_pdf
from models.text_summarization.summarization_model import get_summarization_model, summarize

from python_scripts.pdf_creator.data_schemas import *
from python_scripts.pdf_creator.pdf_creator import PDFCreator

doc_config_path = Path(__file__).parent / "models" / "text_summarization" / "doc_summary_config.yaml"

ORIGINAL_DOCS_FOLDER_PATH = Path(__file__).parent / "models" / "text_summarization" / "docs"
SUMMARIZED_DOCS_FOLDER_PATH = Path(__file__).parent / "models" / "text_summarization" / "summarized_docs"
cfg = read_config(doc_config_path)

# Loading the PDF document to summarize:
doc_name = cfg['doc_to_summarize']
doc_path = ORIGINAL_DOCS_FOLDER_PATH / doc_name
article_content = read_pdf(doc_path=doc_path)

# # Loading the summarization model:
model_cfg = cfg['model_config']
model_path = model_cfg['model_path']
model_args = model_cfg["kwargs"]
# model_args = None

summarization_model = get_summarization_model(model_path=model_path)
summarized_content = summarize(summarization_model, text=article_content, **model_args)
print(summarized_content)
# summarized_content = summarize(summarization_model, text=article_content)

# # Creating the summarized PDF:
title = "The Summarized Article"
department = "Finance"

summarized_doc_name = f"summarized_{doc_name}"
save_path = Path(__file__).parent / SUMMARIZED_DOCS_FOLDER_PATH / summarized_doc_name


document_size = DocumentSizeEnum.A4
document_style = DocumentStyleEnum.LINEAR
text_margin = 72

title = DocumentSection(content=title, font=FontEnum.HELV, font_size=FontSizeEnum.TITLE, text_color=(0.4, 0.4, 0.4))
department_name = DocumentSection(content=f"Department: {department}", font=FontEnum.HELV, font_size=FontSizeEnum.HEADING, text_color=(0.2, 0.2, 0.2))
contact_info = DocumentSection(content="Contact Info: example@domain.com", font=FontEnum.HELV, font_size=FontSizeEnum.SUBHEADING, text_color=(0.2, 0.2, 0.2))
content = DocumentSection(content=summarized_content, font=FontEnum.HELV, font_size=FontSizeEnum.BODY_SMALL, text_color=(0.1, 0.1, 0.1))

sections = [title, department_name, contact_info, content]

my_doc = PDFCreator(document_size=document_size, sections=sections, document_style=document_style, text_margin=text_margin)
my_doc.create_pdf_doc(save_path)

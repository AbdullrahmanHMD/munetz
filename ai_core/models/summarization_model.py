from abc import ABC, abstractmethod
from pathlib import Path
import sys

abs_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(abs_path))

from python_scripts.pdf_creator.pdf_creator import PDFCreator
from python_scripts.pdf_creator.data_schemas import *

# ./summarize path/to/file.pdf -p "find the location of the project described in the file"

class SummarizationModel(ABC):

    def __init__(self, save_path : Path):
        self.save_path = save_path

    @abstractmethod
    def summarize(self, prompt : str, save_output_as_pdf : bool) -> str:
        pass

    @staticmethod
    def save_summarization_as_txt(summarization : str, save_path : Path) -> None:
        with open(save_path, 'wb') as file:
            file.write(summarization)

    @staticmethod
    def save_summarization_as_pdf(summarization : str, save_path : Path) -> None:
        # TODO: Find a way to make those passed in a config file.
        document_size = DocumentSizeEnum.A4
        document_style = DocumentStyleEnum.LINEAR
        text_margin = 72

        title = DocumentSection(content="The Title of the Document", font=FontEnum.HELV, font_size=FontSizeEnum.TITLE, text_color=(0, 0, 0))
        department_name = DocumentSection(content="Department: Finance", font=FontEnum.HELV, font_size=FontSizeEnum.HEADING, text_color=(0, 0, 0))
        content = DocumentSection(content=summarization, font=FontEnum.HELV, font_size=FontSizeEnum.BODY_SMALL, text_color=(0, 0, 0))

        sections = [title, department_name, content]

        pdf_creator = PDFCreator(document_size=document_size, sections=sections, document_style=document_style, text_margin=text_margin)
        pdf_creator.create_pdf_doc(save_path)

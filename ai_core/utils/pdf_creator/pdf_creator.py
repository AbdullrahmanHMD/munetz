import fitz
from pathlib import Path
from typing import List

from utils.pdf_creator.data_schemas import *


class PDFCreator():
    def __init__(self, document_size : DocumentSizeEnum, sections : list, document_style: DocumentStyleEnum, text_margin : int):
        self.document_width = document_size.value.width
        self.document_height = document_size.value.height

        self.sections = sections
        self.margin = text_margin

        if not isinstance(document_style, DocumentStyleEnum):
            raise ValueError(f"Invalid style: {document_style}. Must be one of: {list(DocumentStyleEnum)}")

        self.document_style = document_style

    def add_section(self, new_section : DocumentSection) -> None:
        self.sections.append(new_section)

    def create_linear_sections(self, doc, page):
        section_margin = 10
        line_spacing = 14

        current_margin = self.margin
        max_width = page.rect.width - 2 * self.margin

        for section in self.sections:
            section_content, font_name, font_size, _ = section.content, section.font.value, section.font_size.value, section.text_color

            content_lines = PDFCreator.split_text_to_fit_width(text=section_content, font_name=font_name, font_size=font_size, max_width=max_width)
            page, doc = self.fit_lines_into_width(doc=doc, page=page, content_lines=content_lines, current_margin=current_margin,
                                                  line_spacing=line_spacing, section=section)

            current_margin += font_size + section_margin

        return doc

    def fit_lines_into_width(self, doc, page, content_lines : list, current_margin : int, line_spacing : int, section : DocumentSection):

        for line in content_lines: # TODO: Handle the case where the title is more than one line: the margin is incorrect.
            if current_margin + line_spacing > page.rect.height - self.margin:
                page = doc.new_page(width=self.document_width, height=self.document_height)
                current_margin = self.margin

            font_size, font_name, color = section.font_size.value, section.font.value, section.text_color
            page.insert_text((self.margin, current_margin), line, fontsize=font_size, fontname=font_name, color=color)
            current_margin += line_spacing

        return page, doc


    def create_pdf_doc(self, output_path : Path) -> None:
        doc = fitz.open()
        page = doc.new_page(width=self.document_width, height=self.document_height)
        doc = self.create_linear_sections(doc, page)

        doc.save(output_path)


    @staticmethod
    def split_text_to_fit_width(text : str, font_name : str, font_size : int, max_width : int) -> List:
        font = fitz.Font(font_name)
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = font.text_length(word, font_size)
            space_width = font.text_length(" ", font_size)

            if current_width + word_width + space_width > max_width:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width + space_width

        if current_line:
            lines.append(" ".join(current_line))

        return lines

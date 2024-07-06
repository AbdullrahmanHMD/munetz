import yaml
from pathlib import Path
from typing import Dict
import fitz
from bs4 import BeautifulSoup


def read_config(config_path : Path) -> Dict:
    with open(config_path, 'r') as cfg:
        cfg_file = yaml.safe_load(cfg)
    return cfg_file


def read_pdf(doc_path : Path) -> str:
    content = ""
    with fitz.open(doc_path) as pdf_doc:
        number_of_pages = pdf_doc.page_count
        for page_number in range(number_of_pages):
            page = pdf_doc.load_page(page_number)
            content += page.get_text()
    return content


def read_pdfs(doc_paths : list[Path]) -> list:
    pdfs = []
    for path in doc_paths:
        pdfs.append(read_pdf(path))

    return pdfs


def read_and_parse_html(html_path : Path) -> str:
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.prettify()


def decode_text(text) -> str:
    """Attempt to decode text using multiple encodings."""
    encodings = ['utf-8', 'latin1', 'utf-16', 'utf-32']
    for enc in encodings:
        try:
            return text.decode(enc)
        except (UnicodeDecodeError, AttributeError):
            continue
    return text

import yaml
from pathlib import Path
from typing import Dict
import fitz


def read_config(config_path : Path) -> Dict:
    with open(config_path, 'r') as cfg:
        cfg_file = yaml.safe_load(cfg)
    return cfg_file


def read_pdf(doc_path : Path):
    content = ""
    with fitz.open(doc_path) as pdf_doc:
        number_of_pages = pdf_doc.page_count
        for page_number in range(number_of_pages):
            page = pdf_doc.load_page(page_number)
            content += page.get_text()
    return content


def decode_text(text):
    """Attempt to decode text using multiple encodings."""
    encodings = ['utf-8', 'latin1', 'utf-16', 'utf-32']
    for enc in encodings:
        try:
            return text.decode(enc)
        except (UnicodeDecodeError, AttributeError):
            continue
    return text

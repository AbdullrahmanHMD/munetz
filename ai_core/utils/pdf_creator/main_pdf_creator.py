from data_schemas import *
from pdf_creator import PDFCreator


document_size = DocumentSizeEnum.A4
document_style = DocumentStyleEnum.LINEAR
text_margin = 72

title = DocumentSection(content="The Title of the Document", font=FontEnum.HELV, font_size=FontSizeEnum.TITLE, text_color=(0, 0.9, 0))
department_name = DocumentSection(content="Department: Finance", font=FontEnum.HELV, font_size=FontSizeEnum.HEADING, text_color=(0, 0, 0.8))
subheading_demo = DocumentSection(content="Subheading: subheading demo", font=FontEnum.HELV, font_size=FontSizeEnum.SUBHEADING, text_color=(0.7, 0, 0))

subheading_demo2 = DocumentSection(content="Another Subheading: subheading demo", font=FontEnum.HELV, font_size=FontSizeEnum.SUBHEADING, text_color=(0.7, 0.7, 0))

cont = " ".join(["Lorem ipsum"] * 1500)
content = DocumentSection(content=cont, font=FontEnum.HELV, font_size=FontSizeEnum.BODY_SMALL, text_color=(0, 0, 0))

sections = [title, department_name, subheading_demo, subheading_demo2, content]
# sections = [title, department_name, subheading_demo, content]

my_doc = PDFCreator(document_size=document_size, sections=sections, document_style=document_style, text_margin=text_margin)
my_doc.create_pdf_doc("text_doc.pdf")

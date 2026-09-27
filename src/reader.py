from pypdf import PdfReader as reader
import re

def read_file(pdf_path):
    pdf = reader(pdf_path)

    pages = pdf.pages
    pdf_text = ""
    pdf_text_cleaned = ""
    for page in pages:
        page_text = page.extract_text()
        pdf_text += page_text + "\n"

    #unwanted_char = str.maketrans(".")
    pdf_text = pdf_text.replace(".","")
    pdf_text = re.sub(r"[. ]{3,}","",pdf_text)
    pdf_text_cleaned = pdf_text
    
    return pdf_text_cleaned 

if __name__ == "__main__":
    print("This is a test\n")
    path = input("Please input the path of the pdf you want to extract:\n")
    print(read_file(path))    
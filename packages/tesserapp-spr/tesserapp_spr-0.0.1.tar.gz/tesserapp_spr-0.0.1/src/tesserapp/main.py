import os
import re
import fitz  # PyMuPDF
import pytesseract

# Path to folder containing PDF files
file_in_folder = r"C:\\Users\\steve\\pyStuff\\pytesseract\\filein"

# Check if the folder exists
if not os.path.exists(file_in_folder):
    print(f"Error: The folder '{file_in_folder}' does not exist.")
    exit()

# Set the path to the Tesseract executable
pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Establish regex patterns
regex_filename = r'(\d{6})\.\w+'
regex_ocr = r'\b\d{6}[A-Za-z]{2,}\b'

# Set the company name
co_name = 'POS'

def ocr_core(input_pdf):
    pdf_path = os.path.join(file_in_folder, input_pdf)
    
    # Open the PDF file using PyMuPDF
    pdf_document = fitz.open(pdf_path)

    text = ""
    # Iterate through each page in the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()

    return text

# Iterate through all PDF files in the specified folder
for pdf_file in os.listdir(file_in_folder):
    if pdf_file.endswith(".pdf"):
        # Extract invoice number from filename
        invoice_number_match = re.search(regex_filename, pdf_file)
        invoice_number = invoice_number_match.group(1) if invoice_number_match else ''

        # Run OCR to get PO number
        po_number_text = ocr_core(pdf_file)
        po_number_matches = re.findall(regex_ocr, po_number_text)
        po_number = po_number_matches[0].lower() if po_number_matches else ''

        # Rename the PDF file
        new_filename = f"{co_name} {po_number} {invoice_number}.pdf"
        new_filepath = os.path.join(file_in_folder, new_filename)
        os.rename(os.path.join(file_in_folder, pdf_file), new_filepath)

        print(f"Renamed '{pdf_file}' to '{new_filename}'")
import pymupdf as fitz


def extract_text_from_pdf(pdf_path, output_txt_path):
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)

        # Open the output TXT file in write mode
        with open(output_txt_path, "w", encoding="utf-8") as output_file:
            # Loop through each page in the PDF
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()  # Extract text from the page
                output_file.write(f"Page {page_num + 1}\n{text}\n")

        print(f"Text successfully extracted to {output_txt_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
pdf_path = "AS-001511.pdf"  # Replace with the path to your PDF file
output_txt_path = "output2.txt"  # Replace with the desired output TXT file path
extract_text_from_pdf(pdf_path, output_txt_path)

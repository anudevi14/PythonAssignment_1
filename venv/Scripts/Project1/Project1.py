import os
import PyPDF2

def read_pdf_and_write_to_txt(pdf_path, txt_path):
    # Check if the folder exists
    folder_path = os.path.dirname(pdf_path)
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Check if the PDF file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: PDF file '{pdf_path}' does not exist.")
        return

    # Check if the txt file exists
    if not os.path.isfile(txt_path):
        print(f"Error: PDF file '{txt_path}' does not exist.")
        return

    try:
        # Try to open and read the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            # Extract text from each page of the PDF
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""  # Avoid None if no text found


        # Write the extracted text to the output text file
        with open(txt_path, 'w',encoding='UTF-8') as txt_file:
            txt_file.write(text)

        print(f"Text extracted and written to '{txt_path}' successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the paths for the PDF and output text file
current_directory = os.getcwd()
pdf_path = current_directory+'\\content\\Chemistry Questions.pdf'
txt_path = current_directory+'\\content\\output.txt'

# Call the function to read the PDF and write to output.txt
read_pdf_and_write_to_txt(pdf_path, txt_path)
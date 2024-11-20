import os
import PyPDF2

def extract_pdf_content(pdf_path):
    """Extract text content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            # Extract text from all pages in the PDF
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""  # Avoid None if no text is found
            return text
    except Exception as e:
        print(f"Error reading PDF '{pdf_path}': {e}")
        return None

def process_pdfs_and_write_to_txt(base_folder):
    # Subfolders under the base folder
    subfolders = ['One', 'Two', 'Three']

    # Process each subfolder
    for subfolder in subfolders:
        subfolder_path = os.path.join(base_folder, subfolder)

        # Check if the subfolder exists
        if not os.path.exists(subfolder_path):
            print(f"Error: Subfolder '{subfolder}' does not exist.")
            continue

        # Check if output.txt already exists in the subfolder
        output_txt_path = os.path.join(subfolder_path, 'output.txt')
        if not os.path.exists(output_txt_path):
            print(f"output.txt doesnot exists in '{subfolder}', skipping PDF processing.")
            continue

        # Look for all PDF files in the subfolder
        pdf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.pdf')]

        if len(pdf_files) == 0:
            print(f"Error: No PDF file found in subfolder '{subfolder}'.")
            continue



        with open(output_txt_path, 'w',encoding='UTF-8') as txt_file:  # Opening in 'w' mode to overwrite
            # Process each PDF file in the subfolder
            for pdf_file in pdf_files:
                pdf_file_path = os.path.join(subfolder_path, pdf_file)
                print(f"Processing PDF: {pdf_file_path}")

                # Extract content from the PDF file
                pdf_content = extract_pdf_content(pdf_file_path)

                if pdf_content:
                    # Write the extracted content to output.txt
                    txt_file.write(f"--- Content from {pdf_file} ---\n")
                    txt_file.write(pdf_content + "\n")
                    txt_file.write("\n" + "="*50 + "\n")  # Separator between PDFs
                    print(f"Text content from '{pdf_file_path}' written to '{output_txt_path}'.")
                else:
                    print(f"Failed to extract content from PDF '{pdf_file_path}'.")

current_directory = os.getcwd()
process_pdfs_and_write_to_txt(current_directory+'\\content')
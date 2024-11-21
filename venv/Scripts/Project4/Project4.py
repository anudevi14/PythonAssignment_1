import os
import PyPDF2
import json
import re

def load_config(config_file):

    #Load the configuration file and return the regex pattern.

    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            if "regex" not in config:
                raise KeyError("The configuration must include a 'regex' key.")
            return config["regex"]
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the configuration file '{config_file}'.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while loading the configuration: {e}")
        exit(1)

def extract_page_content_with_regex(pdf_path, txt_path,page_number,regex):
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
            # Check if the page number is valid
            if page_number < 1 or page_number > len(reader.pages):
                print(f"Error: Page number {page_number} is out of range. This PDF has {len(reader.pages)} pages.")
                return
            # Extract content of the specified page
            page = reader.pages[page_number - 1]
            text += page.extract_text() or ""  # Avoid None if no text found

            # Find matches using the regular expression
            matches = re.findall(regex, text)
            matched_content = "\n".join(matches)

            # Write the extracted text to the output text file
            with open(txt_path, 'w',encoding='UTF-8') as txt_file:
                txt_file.write(matched_content)

        print(f"Text extracted and written to '{txt_path}' successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the paths for the PDF and output text file
current_directory = os.getcwd()
pdf_path = current_directory+'\\content\\Chemistry Questions.pdf'
txt_path = current_directory+'\\content\\output.txt'
config_file_path=current_directory+'\\config.json'
# Call the function to read the PDF and write to output.txt
page_number=int(input("Enter the page number: "))
regex =load_config(config_file_path)
extract_page_content_with_regex(pdf_path, txt_path,page_number,regex)
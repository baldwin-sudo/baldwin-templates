import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import argparse


# Load environment variables
def load_environment():
    load_dotenv()

load_environment()
# Set up the LlamaParse parser
def setup_parser(api_key):
    return LlamaParse(
        result_type="text",  # "markdown" and "text" are available
        api_key=api_key,
        show_progress=True
    )

# Define file extractor for different file types
def get_file_extractor(parser):
    return {".pdf": parser}

# Get PDF files from a directory
def get_pdf_files(dir_path):
    return [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.lower().endswith('.pdf')]

# Clean the text by removing extra spaces
def clean_text(text):
    return ' '.join(text.split())

# Convert documents to a string format suitable for writing
def convert_documents_to_string(documents):
    return clean_text(" ".join([doc.text for doc in documents])) if documents else ""

# Write document to a file
def write_document_to_file(document_str, output_file):
    with open(output_file, "w") as file:
        file.write(document_str)

# Process each PDF file
def process_pdf_file(pdf_file, output_dir="texts",parse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")):
    file_name_without_ext = os.path.splitext(os.path.basename(pdf_file))[0]
    output_file = os.path.join(output_dir, f"{file_name_without_ext}.txt")


    #setup parser :
    if not parse_api_key:
        raise ValueError("LLAMA_CLOUD_API_KEY environment variable not set")

    parser = setup_parser(parse_api_key)
    # Use SimpleDirectoryReader to process a single file
    documents = SimpleDirectoryReader(input_files=[pdf_file], file_extractor={".pdf": parser}).load_data()
    document_str = convert_documents_to_string(documents)

    write_document_to_file(document_str, output_file)
    print(f"Processed '{pdf_file}' and saved to '{output_file}'")

# Main function to process all PDF files in a directory
def process_all_pdfs(input_dir, output_dir,parse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")):
    
    
    api_key =parse_api_key
    if not api_key:
        raise ValueError("LLAMA_CLOUD_API_KEY environment variable not set")

    parser = setup_parser(api_key)
    pdf_files = get_pdf_files(input_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in pdf_files:
        process_pdf_file(pdf_file, parser, output_dir)

# If this module is run directly, execute the process_all_pdfs function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF files to text files.")
    parser.add_argument('-i','--input_dir',default="pdfs")
    parser.add_argument('-o','--output_dir',default="texts")
    args = parser.parse_args()
    process_all_pdfs(args.input_dir, args.output_dir)
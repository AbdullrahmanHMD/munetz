import base64
import zipfile
import io
import os
import time
from pathlib import Path

# Define the relative path for the output directory
output_directory = Path(__file__).resolve().parent.parent.parent / 'ai_core/python_scripts/document_summarization/docs'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Read the base64 encoded data from the text file
input_file = Path(__file__).resolve().parent / "zipBinaryContent.txt"
with open(input_file, 'r') as inp:
    base64_data = inp.read()

# Decode the base64 data to get the binary zip file content
zip_data = base64.b64decode(base64_data)

# Use io.BytesIO to create a file-like object from the binary zip data
zip_file = io.BytesIO(zip_data)

# Get the current epoch time as a string
epoch_time = str(int(time.time()))

# List to hold the names of the extracted files
extracted_files = []

# Open the zip file
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    # Iterate over each file in the zip archive
    for file_info in zip_ref.infolist():
        # Get the original file name
        original_filename = file_info.filename
        # Create the new file name with the epoch time prefix
        new_filename = f"{epoch_time}-{original_filename}"
        # Define the full path for the new file
        new_file_path = os.path.join(output_directory, new_filename)
        # Extract and write the file with the new name
        with zip_ref.open(file_info) as source, open(new_file_path, 'wb') as target:
            target.write(source.read())
        # Add the new file name to the list
        extracted_files.append(new_filename)

# Print the names of the extracted files as a comma-separated list
print(",".join(extracted_files))
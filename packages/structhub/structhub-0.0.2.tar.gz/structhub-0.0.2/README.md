# StructHub Client

StructHub Client is a Python package for interacting with the StructHub API.

## Installation

You can install the package using pip:

```
pip install structhub


## Usage

```python
from structhub import StructHubClient

# Initialize the StructHubClient with your API key
api_key = "YOUR_API_KEY_HERE"
client = StructHubClient(api_key)

# File to upload and extract text from
file_path = "path/to/your/file.txt"

# Use the StructHubClient to extract text from the file
extracted_text = client.extract(file_path)

# Print the extracted text
print(extracted_text)


# LICENSE

- MIT License

import mimetypes
import requests
import time
from typing import Optional

class StructHubClient:
    """
    Client for interacting with the StructHub API.

    Attributes:
        api_key (str): The API key for accessing the StructHub API.
        base_url (str): The base URL for the StructHub API calls.
    """

    def __init__(self, api_key: str):
        """
        Initialize the StructHubClient with an API key.

        Args:
            api_key (str): The API key for accessing the StructHub API.
        """
        self.api_key = api_key
        self.base_url = "https://api.structhub.io"

    def extract(self, file_path: str, ocr: str = "auto", lang: Optional[str] = None, out_format: str = "text", max_retries: int = 3) -> str:
        """
        Extracts text from the provided file using the StructHub API.

        Args:
            file_path (str): The path to the file to be uploaded.
            ocr (str): Optional. Set to "auto" (default), "true", or "false" to enable OCR.
            lang (Optional[str]): Optional. Explicitly set the language of the uploaded document.
            out_format (str): Optional. Set the output format to "text", "xml", "json", or "html".
            max_retries (int): Optional. The maximum number of retry attempts for HTTP 429 responses.

        Returns:
            str: The extracted text from the uploaded file.

        Raises:
            Exception: If the request cannot be completed after the specified number of retries.
        """
        url = f"{self.base_url}/extract"
        headers = {'API-KEY': self.api_key}
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        with open(file_path, 'rb') as file_to_upload:
            files = {'file': (file_path, file_to_upload, mime_type)}
            data = {'ocr': ocr, 'out_format': out_format}
            if lang:
                data['lang'] = lang

            for attempt in range(max_retries + 1):
                try:
                    response = requests.post(url, headers=headers, data=data, files=files)
                    if response.status_code == 429 and attempt < max_retries:
                        delay = 2 ** attempt
                        print(f"Too many requests. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        response.raise_for_status()
                        return response.text
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries:
                        raise Exception("Max retries exceeded. Unable to complete the request.") from e
                    print(f"Request failed: {e}. Retrying...")

        raise Exception("Unable to complete the request after retries.")

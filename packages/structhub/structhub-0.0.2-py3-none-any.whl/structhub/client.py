import requests
import time

class StructHubClient:
    """
    Client for interacting with the StructHub API.

    Attributes:
        api_key (str): The API key for accessing the StructHub API.
        base_url (str): The base URL for the StructHub API.
    """

    def __init__(self, api_key):
        """
        Initializes the StructHubClient with the provided API key.

        Args:
            api_key (str): The API key for accessing the StructHub API.
        """
        self.api_key = api_key
        self.base_url = "https://api.structhub.io"

    def extract(self, file_path, ocr="auto", lang=None, out_format="text", max_retries=3):
        """
        Extracts text from the provided file using the StructHub API.

        Args:
            file_path (str): The path to the file to be uploaded.
            ocr (str): Optional. Set to "auto" (default), "true", or "false" to enable Optical Character Recognition (OCR).
            lang (str): Optional. Explicitly set the language of the uploaded document. E.g., "eng+fra" for English and French.
            out_format (str): Optional. Set the output format to "text", "xml", "json", or "html".
            max_retries (int): Optional. The maximum number of retry attempts for HTTP status code 429 (Too Many Requests).

        Returns:
            str: The extracted text from the uploaded file.

        Raises:
            requests.exceptions.RequestException: If there is an error making the request.
            Exception: If max_retries is exceeded and the request cannot be completed.
        """
        url = f"{self.base_url}/extract"
        headers = {'API-KEY': self.api_key}
        files = {'file': open(file_path, 'rb')}
        data = {'ocr': ocr, 'lang': lang, 'out_format': out_format}
        retries = 0
        while retries <= max_retries:
            try:
                response = requests.post(url, headers=headers, files=files, data=data)
                if response.status_code == 429 and retries < max_retries:
                    # Too Many Requests, retry with exponential backoff
                    delay = 2 ** retries
                    print(f"Too many requests. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    retries += 1
                else:
                    response.raise_for_status()
                    return response.text
            except requests.exceptions.RequestException as e:
                # Network errors or other exceptions
                print("Request Exception:", e)
                raise e
        raise Exception("Max retries exceeded. Unable to complete the request.")

import os
import requests

class CMSClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("CMS_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided or found in environment variables")

        self.base_url = self._get_ngrok_link()
        self.validate_key_url = f"{self.base_url}/validateKey"
        self.process_image_url = f"{self.base_url}/processImage"

        # Define error messages for specific status codes
        self.error_messages = {
            400: "Bad Request: Your request is invalid.",
            401: "Unauthorized: Your API key is invalid.",
            # 404: "Not Found: The requested resource was not found.",
            500: "Internal Server Error: We had a problem with our server.",
            # Add more status codes and messages as needed
        }

    def _get_ngrok_link(self):
        # Fetch the ngrok link from the provided URL
        response = requests.get("https://gist.githubusercontent.com/TanmayDoesAI/37c473526f8cdaf2b6e96c5029bd52a6/raw")
        response.raise_for_status()
        ngrok_link = response.text.strip()
        print(ngrok_link)
        return ngrok_link

    def handle_error(self, response):
        # Check if response status code indicates an error
        if response.status_code != 200:
            # Get error message from dictionary or use default message
            error_message = self.error_messages.get(response.status_code, "An error occurred.")
            raise requests.HTTPError(f"HTTP Error {response.status_code}: {error_message}")

    def validate_key(self):
        # Send API key to the validate endpoint
        response = requests.post(self.validate_key_url, json={"key": self.api_key})
        self.handle_error(response)
        return response.json()

    def validate_params(self, params_json):
        # Verify that params_json is in the correct format
        valid_models = ["NSFW", "Gore", "GenAI", "Deepfake"]
        if not all(key in params_json for key in ["model", "image"]) or \
           params_json["model"] not in valid_models:
            raise ValueError("Invalid params format or missing model choice")

        # Set default threshold if not provided
        params_json.setdefault("threshold", 0.65)  # Default threshold is 65%
        return params_json

    def process_image(self, image_url, params_json):
        # Validate the key first
        validation_response = self.validate_key()
        if validation_response.get("status") != "success":
            raise ValueError("API key validation failed")

        # Validate and format params_json
        params_json = self.validate_params(params_json)

        # Send request to processImage endpoint
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"image_url": image_url, "params": params_json}
        response = requests.get(self.process_image_url, headers=headers, json=data)
        self.handle_error(response)
        return response.json()
    
# # Example usage:
# client = CMSClient(api_key="123456")
# image_url = "https://example.com/image.jpg"
# params = {
#     "model": "NSFW",
#     "image": image_url,
#     "threshold": 0.8  # Optional, set custom threshold
# }

# try:
#     result = client.process_image(image_url, params)
#     print(result)
# except Exception as e:
#     print(f"Error: {e}")
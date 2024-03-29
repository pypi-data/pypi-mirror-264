import requests
import os

API_URL = os.getenv("API_URL")
if API_URL is None:
    raise ValueError("API_URL environment variable not set. Please set the API_URL environment variable.")

def api_call(api_key, endpoint, req_type, data=None, files=None):
    endpoint_fmtd = f"/{endpoint}" if not endpoint.startswith("/") else endpoint
    url = f"{API_URL}/{endpoint_fmtd}"

    headers = {
        "X-API-KEY": api_key,
        # "Content-Type": "application/json" # This is set automatically when using files in requests
    }
    if req_type == "POST":
        if files:
            # When uploading files, the 'files' parameter is used in requests.post
            # The 'Content-Type' header is set automatically, so it's omitted here
            response = requests.post(url, headers=headers, files=files, timeout=10)
        else:
            # For regular POST requests with JSON data
            response = requests.post(url, headers=headers, json=data, timeout=10)
    elif req_type == "GET":
        response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        print(f"({req_type}) {endpoint} API Call Successful")
        return response.json()
    else:
        error_message = (
            f"API Call failed with status code: {response.status_code}, "
            f"Error: {response.text}"
        )
        print(error_message)
        return None

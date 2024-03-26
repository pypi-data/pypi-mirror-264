import requests
import json
import threading
import logging
import pdb


class GenOpsClient:
    def __init__(self, hostname, project_id, endpoint_id, project_key, use_https=True):
        self.hostname = hostname
        self.project_id = project_id
        self.endpoint_id = endpoint_id
        self.project_key = project_key
        self.use_https = use_https
        protocol = "https" if self.use_https else "http"
        self.endpoint_url = f"{protocol}://{self.hostname}/api/projects/{self.project_id}/endpoints/{self.endpoint_id}"
        logging.info("Client created")

    def submit(self, **kwargs):
        payload = self.build_payload(**kwargs)
        return self.send_request(payload)

    def submit_async(self, **kwargs):
        payload = self.build_payload(**kwargs)
        threading.Thread(target=self.send_request, args=(payload,)).start()

    def build_payload(self, **kwargs):
        valid_keys = [
            "prompt",
            "response",
            "interaction_id",
            "conversation_id",
            "base64_image",  # gpt-4-vision-preview only
        ]

        payload = {key: value for key, value in kwargs.items() if key in valid_keys}
        payload["project_key"] = self.project_key

        required_keys = ["prompt", "project_key"]
        missing_keys = [key for key in required_keys if key not in payload]
        if missing_keys:
            raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

        return payload

    def send_request(self, payload):
        try:
            response = requests.post(self.endpoint_url, json=payload, verify=True)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error in asynchronous request: {e}")


def connect(hostname, project_id, endpoint_id, project_key, use_https=True):
    if not all(
        isinstance(arg, str) for arg in [hostname, project_id, endpoint_id, project_key]
    ):
        raise TypeError(
            "The 'hostname', 'project_id', 'endpoint_id', and 'project_key' arguments must be strings."
        )
    return GenOpsClient(hostname, project_id, endpoint_id, project_key, use_https)

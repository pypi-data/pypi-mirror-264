import json
from typing import Literal

import requests

from deep_tts.data_models import SupportedProvider


class DeepTTS:
    """
    DeepGrain Text-to-Speech (DeepTTS) service.

    Args:
        access_token (str): The access token for the DeepTTS system.
        provider (Literal["EU", "CN"], optional): The provider of the DeepTTS system. Defaults to "EU".

    Attributes:
        access_token (str): The access token for the DeepTTS system.
        provider (Literal["EU", "CN"]): The provider of the DeepTTS system.

    Methods:
        create(text: str, params: dict) -> str:
            Generates audio for the given text using the specified provider.

    """

    def __init__(self, access_token: str, provider: Literal["EU", "CN"] = "EU"):
        self.access_token = access_token
        self.provider = provider

    def _call_tier_eu(self, params: SupportedProvider.EU):  # noqa: ANN202
        # if self.access_token:

        endpoint = "http://127.0.0.1:8181/eu/tts"

        if params.voice == "test_1":
            params.voice = "alloy"  # type: ignore

        payload = json.dumps(params.model_dump())
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, headers=headers, data=payload, stream=True)

        # Receive the response header with proper decoding
        response_headers = response.headers
        script = response_headers.get("script", "").encode("latin-1").decode("utf-8")
        tokens = response_headers.get("tokens", "")

        # Save the audio data to a file
        file_path = "audio.mp3"
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Request failed with status {response.status_code}.")

        # return "Tier EU - generated audio: " + params.text
        return {"script": script, "tokens": tokens}

    def _call_tier_cn(self, params: SupportedProvider.CN):  # noqa: ANN202
        endpoint = "http://127.0.0.1:8181/cn/tts"

        if params.voice_type == "test_2":
            params.voice_type = "aiyuan"  # type: ignore
        payload = json.dumps(params.model_dump())
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, headers=headers, data=payload, stream=True)

        # Save the audio data to a file
        file_path = "audio.mp3"
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Request failed with status {response.status_code}.")

        return "Tier CN - generated audio for: " + params.text

    def create(self, params: dict):
        # if self.provider == "EU":
        if params.get("voice_id") == "test_1":
            params["voice"] = params.pop("voice_id")  # rename voice_id to voice
            formatted_params = SupportedProvider.EU(**params)
            return self._call_tier_eu(formatted_params)
        # elif self.provider == "CN":
        elif params.get("voice_id") == "test_2":
            params["voice_type"] = params.pop("voice_id")
            formatted_params = SupportedProvider.CN(**params)
            return self._call_tier_cn(formatted_params)

    def stream_text(self, text_data):
        # Open a generator that yields chunks of the text data
        def generate_chunks():
            for chunk in text_data:
                yield chunk.encode()

        # Make a POST request with streamed data
        endpoint = "http://127.0.0.1:8181/eu/upload"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url=endpoint, headers=headers, data=generate_chunks(), stream=True)

        return response

    def stream_status(self, chunk_id: str):
        endpoint = "http://127.0.0.1:8181/eu/upload?chunk_id=" + chunk_id
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url=endpoint, headers=headers, stream=True)

        return response

    def stream_to_file(self, chunk_id: str, file_path: str = "./streamed_audio.mp3"):
        endpoint = "http://127.0.0.1:8181/eu/audio_stream?chunk_id=" + chunk_id
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(endpoint, headers=headers, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Request failed with status {response.status_code}.")

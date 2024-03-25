import json
from typing import Literal

import requests

from deep_tts.data_models import SupportedProvider


class DeepTTS:
    """
    DeepGrain Text-to-Speech (DeepTTS) service.

    Args:
        access_token (str): The access token for the DeepTTS system.
        provider (Literal["OpenAI", "Alibaba"], optional): The provider of the DeepTTS system. Defaults to "OpenAI".

    Attributes:
        access_token (str): The access token for the DeepTTS system.
        provider (Literal["OpenAI", "Alibaba"]): The provider of the DeepTTS system.

    Methods:
        create(text: str, params: dict) -> str:
            Generates audio for the given text using the specified provider.

    """

    def __init__(self, access_token: str, provider: Literal["eu", "cn"] = "eu"):
        self.access_token = access_token
        self.provider = provider

    def _call_openai(self, text: str, params: SupportedProvider.OpenAI):  # noqa: ANN202
        # if self.access_token:

        endpoint = "http://127.0.0.1:8181/openai/tts"
        payload = json.dumps(params.model_dump()).encode("utf-8")
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, headers=headers, data=payload, stream=True)

        # Save the audio data to a file
        file_path = "audio_openai.mp3"
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Request failed with status {response.status_code}.")

        return "OpenAI generated audio: " + text

    def _call_alibaba(self, text: str, params: SupportedProvider.Alibaba):  # noqa: ANN202
        endpoint = "http://127.0.0.1:8181/alibaba/tts"

        payload = json.dumps(params.model_dump())
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, headers=headers, data=payload, stream=True)

        # Save the audio data to a file
        file_path = "audio_alibaba.mp3"
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Request failed with status {response.status_code}.")

        return "Alibaba generated audio for: " + text

    def create(self, text: str, params: dict):
        if self.provider == "OpenAI":
            formatted_params = SupportedProvider.OpenAI(**params)
            return self._call_openai(text, formatted_params)
        elif self.provider == "Alibaba":
            formatted_params = SupportedProvider.Alibaba(**params)  # noqa
            return self._call_alibaba(text, formatted_params)

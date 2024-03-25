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

    def _call_tier_eu(self, text: str, params: SupportedProvider.EU):  # noqa: ANN202
        # if self.access_token:

        endpoint = "http://127.0.0.1:8181/eu/tts"
        payload = json.dumps(params.model_dump()).encode("utf-8")
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, headers=headers, data=payload, stream=True)

        # Save the audio data to a file
        file_path = "audio_tier_eu.mp3"
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Request failed with status {response.status_code}.")

        return "Tier EU - generated audio: " + text

    def _call_tier_cn(self, text: str, params: SupportedProvider.CN):  # noqa: ANN202
        endpoint = "http://127.0.0.1:8181/cn/tts"

        payload = json.dumps(params.model_dump())
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(endpoint, headers=headers, data=payload, stream=True)

        # Save the audio data to a file
        file_path = "audio_tier_cn.mp3"
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Request failed with status {response.status_code}.")

        return "Tier CN - generated audio for: " + text

    def create(self, text: str, params: dict):
        if self.provider == "EU":
            formatted_params = SupportedProvider.EU(**params)
            return self._call_tier_eu(text, formatted_params)
        elif self.provider == "CN":
            formatted_params = SupportedProvider.CN(**params)  # noqa
            return self._call_tier_cn(text, formatted_params)

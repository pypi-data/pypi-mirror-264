from typing import Literal, Optional

from pydantic import BaseModel


class SupportedProvider:
    """Parameters of Supported TTS service providers."""

    class EU(BaseModel):
        voice: Literal["test_1", "test_2"] = "test_1"
        pitch: Optional[str] = ""
        text: str = "Test Test Test, Tier EU TTS Service."

    class CN(BaseModel):
        voice_type: Literal["test_1", "test_2"] = "test_2"
        pitch: Optional[str] = ""
        text: str = "Tier CN TTS 服务。"

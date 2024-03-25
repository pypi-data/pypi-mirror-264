from typing import Literal

from pydantic import BaseModel


class SupportedProvider:
    """Parameters of Supported TTS service providers."""

    class EU(BaseModel):
        stream: bool = True
        model: Literal["tts-1", "tts-1-hd"] = "tts-1"
        voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "alloy"
        text: str = "Test Test Test, OpenAI TTS Service."
        format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "opus"
        description: str = "OpenAI Text-to-Speech (TTS) service"

    class CN(BaseModel):
        stream: bool = True
        voice_type: Literal["aiye", "aimo", "aifan", "aiyuan", "aixiang"] = (
            "aiyuan"
        )
        sample_rate: int = 16000  # TODO: add more supported choices
        format: str = "wav"  # TODO: add more supported choices
        text: str = "测试阿里云TTS服务。"
        description: str = "Alibaba Text-to-Speech (TTS) service"

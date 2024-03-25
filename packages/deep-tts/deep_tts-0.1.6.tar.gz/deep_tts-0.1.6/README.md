# DeepGrain.AI - TTS Service Client

## Install

`pip install deep-tts`

## Usage

```python
import os

from dotenv import load_dotenv

from deep_tts import DeepTTS

load_dotenv(".env")

if __name__ == "__main__":
    tts = DeepTTS(
        access_token=os.getenv("ACCESS_TOKEN") or "",
        provider="OpenAI",
    )

    # 1. Prepare text or stream
    # 2. Call create method: stream = True/False
    # TODO stream text or file
    demo_text = "用户端SDK的调用"
    payload = {
        "stream": True,
        "voice_type": "aiyuan",
    }
    result = tts.create(text=demo_text, params=payload)
    print(result)


```

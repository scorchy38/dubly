import os
from moviepy.editor import *
import requests
import openai


def extract_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)


def transcribe_audio(file_path, api_key, target_language):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    files = {
        "file": (os.path.basename(file_path), audio_data),
        "model": (None, "whisper-1"),
        "language": (None, target_language)
    }

    response = requests.post("https://api.openai.com/v1/audio/transcriptions",
                             headers=headers,
                             files=files)

    if response.status_code == 200:
        result = response.json()
        transcript = result["text"]
        return transcript
    else:
        raise Exception(f"Error: {response.text}")


def translate_text(text, target_language, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"Translate from English to Hindi like a local: {text}",
            },
        ],
    )
    translated_text = response.choices[0].message.content
    print(translated_text)
    return translated_text


def text_to_speech(text, language, output_file):
    elevenlabs_url = "https://api.elevenlabs.io"
    api_path = f"/v1/text-to-speech/yoZ06aMxZJJ28mfd3POQ"
    api_key = "60e3ddabf92db5dbffaca19b1e4e7619"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v1"
    }

    response = requests.post(elevenlabs_url + api_path, headers=headers, json=data)

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Error: {response.text}")


def overlay_audio(video_file, audio_file, output_file):
    video = VideoFileClip(video_file)
    new_audio = AudioFileClip(audio_file)
    final_video = video.set_audio(new_audio)
    final_video.write_videofile(output_file)


def main():
    input_video = "input_video.mp4"
    extracted_audio = "audio.wav"
    api_key = "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"
    source_language = "en"
    target_language = "hi"
    translated_audio = "translated_audio.mp3"
    output_video = "output_video.mp4"

    extract_audio(input_video, extracted_audio)
    transcript = transcribe_audio(extracted_audio, api_key, source_language)
    translated_text = translate_text(transcript, target_language, api_key)
    text_to_speech(translated_text, target_language, translated_audio)
    overlay_audio(input_video, translated_audio, output_video)


if __name__ == "__main__":
    main()

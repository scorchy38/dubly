from moviepy.editor import *
import requests
from googletrans import Translator
from gtts import gTTS


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
        print(transcript)
        return transcript
    else:
        raise Exception(f"Error: {response.text}")



def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text


def text_to_speech(text, language, output_file):
    tts = gTTS(text=text, lang=language)
    tts.save(output_file)


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
    translated_text = translate_text(transcript, target_language)
    text_to_speech(translated_text, target_language, translated_audio)
    overlay_audio(input_video, translated_audio, output_video)


if __name__ == "__main__":
    main()

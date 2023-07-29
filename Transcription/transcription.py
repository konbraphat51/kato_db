import whisper
from pytube import YouTube, Channel
import pandas as pd


video_url = "https://www.youtube.com/watch?v=enmam5ad6b8"

audio_file = YouTube(video_url).streams.filter(
    only_audio=True).first().download(filename="audio.mp4")

whisper_model = whisper.load_model("base")
transcription = whisper_model.transcribe(audio_file, language="ja", task="trascribe")

df = pd.DataFrame(data=transcription['segments'], columns=['start', 'end', 'text'])

print(df)

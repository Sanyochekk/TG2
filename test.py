
#------------------------------------------------------------

from pytube import YouTube
import moviepy.editor as mp
import os


url_youtube = YouTube("https:/www/.youtube.com/watch?v=ex9tML6udCU")


video_stream = url_youtube.streams.filter(only_audio=True).first()


save_folder = r"C:\Users\LOGIKA"



video_file_path = video_stream.download(output_path=save_folder)

base, ext = os.path.splitext(video_file_path)
new_file = base + '.mp3'
os.rename(video_file_path, new_file)
# os.remove(video_file_path)

print(f"Аудиофайл успешно сохранен в {video_file_path}")


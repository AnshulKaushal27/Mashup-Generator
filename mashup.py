import os
import yt_dlp
from pydub import AudioSegment
import zipfile
import tempfile
import shutil


def create_mashup(singer_name, num_videos, duration, output_filename):
    try:
        temp_dir = tempfile.mkdtemp()
        download_path = os.path.join(temp_dir, "downloads")
        os.makedirs(download_path, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }


        search_query = f"{singer_name} popular song -live -mashup -dj"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch{num_videos}:{search_query}"])

        final_audio = AudioSegment.empty()

        files_found = False

        for file in os.listdir(download_path):
            if file.endswith(".mp3"):
                files_found = True
                audio = AudioSegment.from_mp3(os.path.join(download_path, file))

                if duration == 0:
                    final_audio += audio
                else:
                    final_audio += audio[:duration * 1000]

        if not files_found:
            return None, None, "No songs were downloaded."

        output_mp3 = os.path.join(temp_dir, f"{output_filename}.mp3")
        final_audio.export(output_mp3, format="mp3")

        output_zip = os.path.join(temp_dir, f"{output_filename}.zip")
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            zipf.write(output_mp3, os.path.basename(output_mp3))

        return output_mp3, output_zip, None

    except Exception as e:
        return None, None, str(e)


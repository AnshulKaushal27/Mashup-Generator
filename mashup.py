import os
import yt_dlp
from pydub import AudioSegment
import zipfile
import tempfile
import shutil


def create_mashup(singer_name, num_videos, duration, output_filename):

    try:
        # Create unique temporary working directory
        temp_dir = tempfile.mkdtemp()
        download_path = os.path.join(temp_dir, "downloads")
        os.makedirs(download_path, exist_ok=True)

        # yt-dlp options (deployment safe)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'quiet': True,
            'match_filter': lambda info, *, incomplete: (
                None if info.get('duration', 0) <= 600 else 'Video longer than 10 minutes'
            ),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        search_query = f"{singer_name} popular song -live -mashup -dj"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch{num_videos}:{search_query}"])

        # Merge songs
        final_audio = AudioSegment.empty()

        for file in os.listdir(download_path):
            if file.endswith(".mp3"):
                file_path = os.path.join(download_path, file)
                audio = AudioSegment.from_mp3(file_path)

                if duration == 0:
                    final_audio += audio
                else:
                    trimmed = audio[:duration * 1000]
                    final_audio += trimmed

        output_mp3 = os.path.join(temp_dir, f"{output_filename}.mp3")
        final_audio.export(output_mp3, format="mp3")

        # Create zip
        output_zip = os.path.join(temp_dir, f"{output_filename}.zip")
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            zipf.write(output_mp3, os.path.basename(output_mp3))

        return output_mp3, output_zip, temp_dir

    except Exception as e:
        return None, None, str(e)

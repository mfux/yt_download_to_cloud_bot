import pexpect
import os
from pathlib import Path
from time import sleep

class YTDownloader:
    def __init__(self, temp_storage_path):
        self.temp_storage_path = temp_storage_path

    def build_command(self, video_id):
        return f"youtube-dl  https://youtu.be/{video_id} --extract-audio --audio-format mp3 --audio-quality 2 -o '{self.temp_storage_path}/%(title)s.%(ext)s'"

    def download(self, video_id):
        # get files to check later if a file was added
        num_files = len([f for f in os.listdir(self.temp_storage_path) if f.endswith(".mp3")])
        
        # issue download command
        command = self.build_command(video_id)
        pexpect.run(command, timeout=60*20)
        sleep(1)

        # check if download worked
        if len([f for f in os.listdir(self.temp_storage_path) if f.endswith(".mp3")]) > num_files:
            sorted_files = sorted(Path(self.temp_storage_path).iterdir(), key=os.path.getmtime)
            sorted_mp3_files = [str(f) for f in sorted_files if str(f).endswith(".mp3")]

            return sorted_mp3_files[0].replace(f"{self.temp_storage_path}/", "")
        else:
            return ""

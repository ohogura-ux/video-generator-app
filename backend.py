import pyttsx3
import subprocess
import os
from datetime import datetime

class VideoGenerator:
    def __init__(self, output_dir='videos'):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def text_to_speech(self, text, audio_file):
        try:
            engine = pyttsx3.init()
            engine.save_to_file(text, audio_file)
            engine.runAndWait()
        except Exception as e:
            print(f'Error in text_to_speech: {e}')

    def generate_video(self, audio_file, background_file=None):
        try:
            output_file = os.path.join(self.output_dir, f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4')
            if background_file is None:
                background_file = self.create_black_background_video()
            command = [
                'ffmpeg',
                '-i', audio_file,
                '-i', background_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-strict', 'experimental',
                '-shortest',
                output_file
            ]
            subprocess.run(command, check=True)
        except Exception as e:
            print(f'Error in generate_video: {e}')

    def create_black_background_video(self, duration=5):
        try:
            black_video_file = os.path.join(self.output_dir, 'black_background.mp4')
            command = [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', 'color=c=black:s=1280x720:d=' + str(duration),
                '-c:v', 'libx264',
                '-t', str(duration),
                black_video_file
            ]
            subprocess.run(command, check=True)
            return black_video_file
        except Exception as e:
            print(f'Error in create_black_background_video: {e}')


import yt_dlp
import json
import os, shutil

from main import *

class AppFunctions(MainWindow):

    def getTitle(link):
        ydl_opts = {
            'outtmpl': f'temp/info',
            'writeinfojson': 'True',
            'skip_download': 'True', }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        with open('temp/info.info.json') as file:
            dados = json.load(file)
            title = dados['title']
        for item in os.listdir('temp'):
            if os.path.isfile(f"temp/{item}"): os.unlink(f"temp/{item}")
            elif os.path.isdir(f"temp/{item}"): shutil.rmtree(f"temp/{item}")
        return title.replace('/','_')

    def downloadVideo(link, downloadFolder, self):
        global widgets
        widgets = self.widgets
        ydl_opts = {
            # 'skip_download': 'True',
            'progress_hooks': [AppFunctions.my_hook],
            'noplaylist': 'True',
            'ffmpeg_location': 'bin/',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{downloadFolder}{AppFunctions.getTitle(link)}', }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])


    def my_hook(hook):
        if hook['status'] == 'finished':
            widgets.label_3.setText("finished")
        if hook['status'] == 'downloading':
            widgets.label_3.setText("downloading")
            widgets.label_2.setText(hook['_percent_str'])
            widgets.label.setText(hook['_speed_str'])
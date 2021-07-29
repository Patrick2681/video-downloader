
import yt_dlp
import json
import os, shutil

from main import *
import pathlib

class AppFunctions(MainWindow):

    def saveLocation(self):
        if pathlib.Path(f'{pathlib.Path.home()}/Downloads').exists():
            return str(f'{pathlib.Path.home()}/Downloads/video downloader')
        else:
            return str(f'{os.getcwd()}/Downloads')

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
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{downloadFolder}{AppFunctions.getTitle(link)}', }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])


    def my_hook(hook):
        if hook['status'] == 'finished':
            widgets.status.setText("finished")
        if hook['status'] == 'downloading':
            widgets.status.setText("downloading")
            widgets.percentage.setText(hook['_percent_str'])
            widgets.speed.setText(hook['_speed_str'])
import os.path
import re
# import subprocess
from .download import download
from .source import get_videos_audios, get_videos_audios_by_ep_id
from .page import get_page_by_bv
from lxml.etree import HTML
from . import BType

class Episode:

    def __init__(self, collection: str, title: str, cover: str, BV: str, p: int | None, cookie: str = "", btype: int = -1):
        self.__height = None
        self.__collection = re.sub(r"[|\\/<>:*?\"\s]", "-", collection)
        self.__title = re.sub(r"[|\\/<>:*?\"\s]", "-", title)
        self.__cover = cover
        self.__BV = BV
        self.__p = p
        page = ""
        if btype == BType.BANGUMI:
            self.__videos, self.__audios = get_videos_audios_by_ep_id(p, cookie=cookie)
        else:
            page = get_page_by_bv(self.__BV, p=self.__p, cookie=cookie)
            self.__videos, self.__audios = get_videos_audios(HTML(page))

    def getTitle(self):
        return self.__title

    def getHeights(self):
        return list(self.__videos.keys())

    def setHeight(self, height: int):
        self.__height = height

    def download(self, video_flag=False, frames_flag=False, audio_flag=False, cover_flag=False):
        if self.__height is None:
            height = max(self.__videos.keys())
        else:
            height = self.__height
        video = self.__videos[height]
        audio = self.__audios.popitem()[1]
        if not os.path.exists(self.__collection):
            os.makedirs(self.__collection)
        vp = ".\\" + os.path.join(self.__collection, self.__title + "_v.mp4")
        ap = ".\\" + os.path.join(self.__collection, self.__title + "_a.mp3")
        cp = ".\\" + os.path.join(self.__collection, self.__title + "_封面.jpg")
        out = ".\\" + os.path.join(self.__collection, self.__title + ".mp4")
        if cover_flag:
            print("正在下载封面...")
            self.__cover = "https://" + self.__cover.split("//")[1]
            download(self.__cover, cp)
        if frames_flag or video_flag:
            print("正在下载画面...")
            download(video, vp)
        if audio_flag or video_flag:
            print("正在下载音频...")
            download(audio, ap)
        if video_flag:
            print("正在合并音频画面...")
            cmd = f"ffmpeg -i {vp} -i {ap} -c copy {out} -loglevel quiet"
            os.system(cmd)
            # p = subprocess.Popen(cmd, stdin=subprocess.PIPE, close_fds=True)
            # p.communicate("y\n".encode())
            # p.stdin.close()
            # p.kill()
            # p.wait()
            print("合成完毕!")
        if not frames_flag and video_flag:
            os.remove(vp)
        if not audio_flag and video_flag:
            os.remove(ap)


if __name__ == '__main__':
    # Episode("")
    pass

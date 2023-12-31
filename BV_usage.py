import pprint
from utils.BV import BV

bv = BV("BV17s411D7zb", "cookie.txt")
# 打印视频信息
pprint.pprint(bv.getInfo())

# 下载
bv.getEpisode(2).download(
    video_flag=True,  # 保存视频
    frames_flag=False,  # 只保存画面，不保存音频
    audio_flag=False,  # 只保存音频
    cover_flag=False  # 下载封面
)

# 直接下载
# bv.getDirectEpisode()

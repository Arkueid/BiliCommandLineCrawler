import argparse
import re
import sys

from utils.exceptions import *
from _for_bv import _download
from utils.cookie import getCookie

# 命令配置信息
description = "Bilibili命令行爬虫"

parser = argparse.ArgumentParser(
    description=description
)
parser.add_argument("bv", help="视频bv号")
parser.add_argument("-ls", "--list", action="store_true", help="从列表中选择")
parser.add_argument("-v", "--video", action="store_true", help="下载视频")
parser.add_argument("-f", "--frames", action="store_true", help="下载无音频的画面")
parser.add_argument("-a", "--audio", action="store_true", help="下载音频")
parser.add_argument("-c", "--cover", action="store_true", help="下载封面")
parser.add_argument("-p", "--part", nargs=1, type=int, help="分P视频集数")
parser.add_argument("-u", "--cookie", type=str, help="cookie.txt路径")

args = parser.parse_args()

if args.bv:
    bv = re.findall("[BV|bv][0-9a-zA-Z]{11}", args.bv)
    if not any((args.video, args.audio, args.frames, args.cover)):
        print("未选择下载内容, 程序退出")
        sys.exit()
    part = args.part[0] if args.part else None
    cookie = ""
    if args.cookie:
        cookie = getCookie(args.cookie)
    if bv:
        try:
            _download(bv,
                      video=args.video,
                      audio=args.audio,
                      frames=args.frames,
                      cover=args.cover,
                      part=part,
                      list_flag=args.list,
                      cookie=cookie
                      )
        except KeyboardInterrupt:
            print("\n感谢使用")
        except InvalidInput as e:
            print(e)
        except IndexOutOfBoundary as e:
            print(e)
        # except KeyError as e:
        #     print(e)
        #     print("视频不存在，或视频需要大会员账号")
    else:
        print("输入不合法")

elif args.crawl:
    print(args.crawl)

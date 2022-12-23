import json
from lxml.etree import HTML
from . import BType


# 预处理
def get_source_dict(source_page: HTML) -> dict:
    res_ls = source_page.xpath("//script[contains(text(), 'window.__playinfo__=')]/text()")
    res_string = res_ls[0].strip("window.__playinfo__=")
    # print(res_string)
    return json.loads(res_string)


def get_info_dict(source_page: HTML) -> dict:
    res_ls = source_page.xpath("//script[contains(text(), 'window.__INITIAL_STATE__=')]/text()")
    res_string = res_ls[0].strip("window.__INITIAL_STATE__=").replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());", "")
    return json.loads(res_string)


def parse_type(source_dict: dict)->int:
    if "epList" in source_dict:
        return BType.BANGUMI  # 番剧
    elif len(source_dict['sections']) > 0:
        return BType.COLLECTIONS  # 合集
    elif len(source_dict['videoData']['pages']) > 0:
        return BType.EPISODE  # 分集


# 正式接口
def get_videos_audios(source_page: HTML):
    """
    获取视频、音频资源链接
    :param source_page:
    :return:
    """
    js = get_source_dict(source_page)
    # 视频信息
    # video = (分辨率, 基本链接)
    videos = dict()
    for i in js['data']['dash']['video']:
        videos[i['height']] = i['base_url']
    # 音频信息
    audios = dict()
    for i in js['data']['dash']['audio']:
        audios[i['codecs']] = i['base_url']
    return videos, audios


def get_info(source_page: HTML):
    """
    获取视频信息
    :param source_page:
    :return:
    """
    js = get_info_dict(source_page)
    btype = parse_type(js)
    res = None
    if btype == BType.EPISODE:
        info = js['videoData']
        owner = info['owner']['name']
        bvid = info['bvid']
        desc = info['desc']
        pages = list()
        for i in js['videoData']['pages']:
            pages.append(
                {
                    "标题": i['part'],
                    "页码": i['page'],
                }
            )
        res = {
            "合集名称": info['title'],
            "up主": owner,
            "BV": bvid,
            "简介": desc,
            "封面": info['pic'],
            "列表": pages
        }
    elif btype == BType.COLLECTIONS:
        info = js['videoData']
        owner = info['owner']['name']
        title = info['ugc_season']['title']
        episodes = list()
        for i in js['sections'][0]['episodes']:
            episodes.append(
                {
                    "标题": i['title'],
                    "BV": i['bvid'],
                    "封面": i['arc']['pic']
                }
            )
        res = {
            "合集名称": title,
            "up主": owner,
            "列表": episodes
        }
    elif btype == BType.BANGUMI:
        title = js['mediaInfo']['season_title']
        episodes = list()
        for i in js['epList']:
            episodes.append(
                {
                    "标题": i['long_title'],
                    "BV": i['bvid'],
                    "封面": i['cover']
                }
            )
        res = {
            "合集名称": title,
            "up主": "",
            "列表": episodes
        }
    return btype, res


if __name__ == '__main__':
    source = open("hi.html", 'rb').read().decode()
    source = HTML(source)


import json
from lxml.etree import HTML
from . import BType
import re
import requests

# 预处理
def get_source_dict(source_page: HTML) -> dict:
    res_ls = source_page.xpath("//script[contains(text(), 'window.__playinfo__=')]/text()")
    res_string = res_ls[0].strip("window.__playinfo__=")
    # print(res_string)
    return json.loads(res_string)


def get_info_dict(source_page: HTML) -> dict:
    res_ls = source_page.xpath("//script[contains(text(), 'window.__INITIAL_STATE__=')]/text()")
    if len(res_ls) == 0:
        res_ls = source_page.xpath("//script[@id='__NEXT_DATA__']/text()")
        res_string = res_ls[0]

        # 测试
        # with open("123.json", 'w', encoding='utf-8') as f:
        #     f.write(res_string)
    else:
        res_string = res_ls[0].strip("window.__INITIAL_STATE__=").replace(";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());", "")
    return json.loads(res_string)


def parse_type(source_dict: dict)->int:
    if len(source_dict.get('sections', [])) > 0:
        return BType.COLLECTIONS  # 合集
    elif len(source_dict.get('videoData', {}).get('pages', [])) > 0:
        return BType.EPISODE  # 分集
    elif len(source_dict.get('props', {})
                .get('pageProps', {})
                .get('dehydratedState', {})
                .get('queries', [])
             ) > 0:
        return BType.BANGUMI


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

def get_videos_audios_by_ep_id(ep_id: int, cookie: str = ""):
    # print(ep_id)
    url = "https://api.bilibili.com/pgc/player/web/v2/playurl?support_multi_audio=true&qn=0&fnver=0&fnval=4048&fourk=1&gaia_source=&from_client=BROWSER&ep_id=%d&drm_tech_type=2" % ep_id
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "origin": "https://www.bilibili.com/",
        "referer": url,
        "cookie": cookie  # 加入cookie可以获取更高画质
    }
    rsp = requests.get(url, headers=headers)

    js = rsp.json()

    # 测试
    # with open('456.json', 'w', encoding='utf-8') as f:
    #     f.write(rsp.text)

    js = js['result']['video_info']

    videos = dict()
    for i in js['dash']['video']:
        videos[i['height']] = i['base_url']
    # 音频信息
    audios = dict()
    for i in js['dash']['audio']:
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
        js = js['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['seasonInfo']['mediaInfo']
        title = js['season_title']
        episodes = list()
        for i in js['episodes']:
            episodes.append(
                {
                    "标题": i['long_title'],
                    "BV": i['bvid'],
                    "封面": i['cover'],
                    "cid": i['cid'],
                    "aid": i['aid'],
                    "ep_id": i['ep_id']
                }
            )
        res = {
            "合集名称": title,
            "up主": "",
            "列表": episodes
        }
    return btype, res


if __name__ == '__main__':
    import page as page
    source = page.get_page_by_bv("BV1hT4y1R79R")
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(source)
        f.close()

    source = HTML(source)
    source = get_source_dict(source)


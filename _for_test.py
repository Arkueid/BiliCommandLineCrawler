import json
import re

import requests


def get_by_bv(bv:str):
    url = f"https://www.bilibili.com/video/{bv}/"
    headers = {
        # "user-agent": "",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "origin": "https://www.bilibili.com/bangumi/play/ep66523?",
        "referer": url,
        "cookie": "DedeUserID=31373462; Path=/ Domain=biligame.com; Expires=Fri, 24 May 2024 05:25:43 GMT; Secure; SameSite=None;DedeUserID__ckMd5=63c695a16baa608b; Path=/; Domain=biligame.com; Expires=Fri, 24 May 2024 05:25:43 GMT; Secure; SameSite=None;SESSDATA=cfba2479%2C1716528343%2Cd76d9%2Ab1CjAIxwHNgWs6s-auRKCkS8Ev0ogmLKWWhlL6Vw_OGqQRmHeQuwfdsul8iVILae3pQwoSVl9KOWhDdG1nN3dXeUdremk4Q2Y5S1ZseWtJMzlTZHVXN2puMmhicV8xNzE3ejRSNjczT013VkJyTnhSR2h1WUhXTDlCa3JPUTJWVGZ4SmZBZVU3d1VRIIEC; Path=/; Domain=biligame.com; Expires=Fri, 24 May 2024 05:25:43 GMT; HttpOnly; Secure; SameSite=None;bili_jct=6cb13915d51179badcaccd331ee82753; Path=/; Domain=biligame.com; Expires=Fri, 24 May 2024 05:25:43 GMT; Secure; SameSite=None;sid=6a0vjjqo; Path=/; Domain=biligame.com; Expires=Fri, 24 May 2024 05:25:43 GMT; Secure; SameSite=None;"
    }
    rsp = requests.get(url, headers=headers)
    with open("hi.html", 'wb') as f:
        f.write(rsp.content)
    x = re.findall("<script>window.__playinfo__=(.*)</script><script>window.__INITIAL_STATE__=", rsp.text)[0]
    x = json.loads(x)
    for i in x['data']['dash']['video']:
        print(i['height'])


if __name__ == '__main__':
    import pprint
    from utils.BV import BV
    bv = BV("BV17s411D7zb")
    pprint.pprint(bv.getInfo())
    bv.getEpisode(2).download()
"""
获取源网页
"""

import requests


def get_page_by_bv(BV: str, p=None, cookie=""):
    url = "https://www.bilibili.com/video/" + BV + "/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "origin": "https://www.bilibili.com/",
        "referer": url,
        "cookie": cookie  # 加入cookie可以获取更高画质
    }
    params = {"p": p} if p else None
    rsp = requests.get(url, headers=headers, params=params)
    # print("[request url]:", rsp.url)
    return rsp.text


if __name__ == '__main__':
    html = get_page_by_bv("BV1tN411n7un")
    with open("hi.html", "wb") as f:
        f.write(html.encode())


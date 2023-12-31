import time

import requests


def progressbar(cur, total, dur):
    if cur >= total:
        print("\r下载完毕: " + "[%s%s]" % (
            int(cur / total * 20) * "▊", int((total - cur) / total * 20) * " ") + "大小: %.2f/%.2fM 耗时: %.2fs" % (
                  total, total, dur))
    else:
        print("\r正在下载: " + "[%s%s]" % (
            int(cur / total * 20) * "▊", int((total - cur) / total * 20) * " ") + "大小: %.2f/%.2fM 耗时: %.2fs" % (
                  cur, total, dur), end='')


def download(url: str, fpath: str):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36",
        "referer": "https://www.bilibili.com",
    }
    rsp = requests.get(url, headers=headers, stream=True)
    total = eval(rsp.headers.get("content-length")) / 1024000
    iter_content = rsp.iter_content(chunk_size=64 * 1024)
    cur = 0
    with open(fpath, "wb") as f:
        start = time.perf_counter()
        for i in iter_content:
            if i:
                f.write(i)
                cur += 64 * 1024 / 1024000
                progressbar(cur, total, time.perf_counter() - start)
            else:
                break


if __name__ == '__main__':
    download(
        "https://cn-zjhz-cm-01-24.bilivideo.com/upgcxcode/74/46/4804674/4804674_da7-1-100023.m4s?e"
        "=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1671706101&gen=playurlv2&os=bcache&oi=0&trid=0000cc19eaa0e96d428ba721d62e99078727u&mid=0&platform=pc&upsig=09f13edd77d065788a046337f7afc707&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=40059&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&agrr=1&bw=47568&logo=80000000",
        "", "")

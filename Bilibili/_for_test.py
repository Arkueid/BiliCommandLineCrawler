import json
import re

import requests


def get_by_bv(bv:str):
    url = f"https://www.bilibili.com/video/{bv}/"
    headers = {
        # "user-agent": "",
        "cookie": "_uuid=2AD638CA-3843-D4FE-6787-E81410BF46103C44062infoc; b_nut=1658552345; buvid3=F3594E0F-861D-9346-704E-E1222D17029646052infoc; buvid_fp_plain=undefined; DedeUserID=31373462; DedeUserID__ckMd5=63c695a16baa608b; b_ut=5; CURRENT_BLACKGAP=0; go_old_video=1; hit-dyn-v2=1; nostalgia_conf=2; buvid4=561D3EE7-C91D-FA0A-34CB-D8AF3DA4C3E046052-022072312-Pk1O31qDhl5Afas758c5HH6QObg/AbBOaM4znKfjwC6zdUxYNxk6tA==; LIVE_BUVID=AUTO9216589102595540; fingerprint3=5fa93d44f6cf108993dddb4826123102; ogv_channel_version=v1; i-wanna-go-feeds=-1; i-wanna-go-back=2; blackside_state=1; hit-new-style-dyn=0; rpdid=0zbfPWeze1|6JkSf7RM|1qd|3w1OWouX; fingerprint=3335d1c3b8e806bbf0f67784d6392bf3; buvid_fp=3335d1c3b8e806bbf0f67784d6392bf3; CURRENT_FNVAL=4048; CURRENT_QUALITY=80; bp_video_offset_31373462=742713267167690792; PVID=1; SESSDATA=e6eb2e48,1687333984,16982*c2; bili_jct=1e3d5a2f9d2cc79747c7c918278d2b44; sid=6se5s6i6; b_lsid=5BE1F41D_1853E3BC0A6; innersign=1"
    }
    rsp = requests.get(url, headers=headers)
    x = re.findall("<script>window.__playinfo__=(.*)</script><script>window.__INITIAL_STATE__=", rsp.text)[0]
    x = json.loads(x)
    for i in x['data']['dash']['video']:
        print(i['height'])


if __name__ == '__main__':
    get_by_bv("BV1rP4y1B76L")
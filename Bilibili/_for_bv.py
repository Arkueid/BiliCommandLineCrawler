from utils.exceptions import IndexOutOfBoundary, InvalidInput
from utils.BV import BV
from utils import BType


def _download(bv, video=False, audio=False, frames=False, cover=False, part: int | None = None, list_flag=False):
    bv = BV(bv[0])

    info = bv.getInfo()

    total = len(info['列表'])

    print("名称: %s" % info["合集名称"])
    if bv.getBType() == BType.EPISODE:
        desc = "分P视频"
    elif bv.getBType() == BType.COLLECTIONS:
        desc = "视频合集"
    elif bv.getBType() == BType.BANGUMI:
        desc = "番剧"
    else:
        desc = None
    print("类型: %s" % desc) if desc else None
    print("up主: %s" % info["up主"]) if info["up主"] != "" else None

    if list_flag or (not part and bv.getBType() == BType.EPISODE and len(info['列表']) > 1):

        for idx, item in enumerate(info["列表"]):
            print("%2s" % (idx + 1), item["标题"])

        try:
            idx = int(input("请选择视频: "))
        except Exception:
            raise InvalidInput

        if idx <= 0 or idx > total:
            raise IndexOutOfBoundary

        ep = bv.getEpisode(idx - 1)

    elif part:
        if bv.getBType() == BType.EPISODE:

            if part <= 0 or part > total:
                raise IndexOutOfBoundary

            ep = bv.getEpisode(part - 1)

        else:
            raise InvalidInput

    else:
        ep = bv.getDirectEpisode()

    print("当前视频:", ep.getTitle())

    if frames or video:
        hmap = dict()
        for idx, height in enumerate(ep.getHeights()):
            print("%2s" % (idx + 1), str(height) + "P")
            hmap[idx + 1] = height
        try:
            idx = int(input("请选择码率: "))
        except Exception:
            raise InvalidInput

        if idx not in hmap:
            raise IndexOutOfBoundary

        ep.setHeight(hmap[idx])
    ep.download(video_flag=video, audio_flag=audio, frames_flag=frames, cover_flag=cover)


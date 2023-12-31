import pprint

from lxml.etree import HTML

from . import BType
from .episode import Episode
from .exceptions import EpisodeNotFound
from .page import get_page_by_bv
from .source import get_info


class BV:
    cookie = ""

    def __init__(self, bvid: str, cookie: str = ""):
        self.__BV = bvid
        self.cookie = cookie
        source_page = get_page_by_bv(bvid, cookie=cookie)
        source_page = HTML(source_page)
        # pprint.pprint(get_info_dict(source_page))
        self.__type, self.__info = get_info(source_page)

    def getInfo(self):
        return self.__info

    def getBType(self):
        return self.__type

    def getDirectEpisode(self):
        if self.__type == BType.COLLECTIONS:
            for i in self.__info['列表']:
                if i['BV'] == self.__BV:
                    return Episode(self.__info['合集名称'], i['标题'], i['封面'], self.__BV, None, cookie=self.cookie,
                                   btype=self.__type)
        elif self.__type == BType.EPISODE:
            i = self.__info['列表'][0]
            return Episode(self.__info['合集名称'], i['标题'], self.__info['封面'], self.__BV, i['页码'],
                           cookie=self.cookie, btype=self.__type)
        elif self.__type == BType.BANGUMI:
            item = None
            for i in self.__info['列表']:
                if i['BV'] == self.__BV:
                    item = i
                    break
            if item is None:
                raise EpisodeNotFound
            return Episode(self.__info['合集名称'], item['标题'], item['封面'], self.__BV, item['ep_id'],
                           cookie=self.cookie, btype=self.__type)

    def getEpisode(self, idx):
        ep = self.__info['列表'][idx]
        if self.__type == BType.COLLECTIONS:
            collection = self.__info['合集名称']
            title = ep['标题']
            bvid = ep['BV']
            p = None
            cover = ep["封面"]
        elif self.__type == BType.EPISODE:
            collection = self.__info['合集名称']
            title = ep['标题']
            bvid = self.__info['BV']
            p = ep['页码']
            cover = self.__info["封面"]
        elif self.__type == BType.BANGUMI:
            ep = self.__info['列表'][idx]
            collection = self.__info['合集名称']
            title = ep['标题']
            bvid = ep['BV']
            p = ep['ep_id']
            cover = ep["封面"]
        else:
            return None
        return Episode(collection, title, cover, bvid, p, self.cookie, btype=self.__type)


if __name__ == '__main__':
    bv = BV("BV17s411D7zb")
    pprint.pprint(bv.getInfo())
    bv.getEpisode(2).download()

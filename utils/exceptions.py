class IndexOutOfBoundary(Exception):

    def __init__(self):
        super().__init__("输入超出范围")


class InvalidInput(Exception):

    def __init__(self):
        super().__init__("输入不合法")

class InvalidCookiePath(Exception):

    def __init__(self):
        super().__init__("cookie 文件应为文本格式")

class EpisodeNotFound(Exception):

    def __init__(self):
        super().__init__("视频列表为空")
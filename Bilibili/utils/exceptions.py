class IndexOutOfBoundary(Exception):

    def __init__(self):
        super().__init__("输入超出范围")


class InvalidInput(Exception):

    def __init__(self):
        super().__init__("输入不合法")


import os
from .exceptions import InvalidCookiePath


def getCookie(path: str) -> str:
    ext = os.path.splitext(path)
    if ext[1] == ".txt" or ext[1] == "":
        if os.path.exists(path):
            with open(path, 'r', encoding="utf-8-sig") as f:
                cookie = f.read()
        else:
            raise FileNotFoundError
    else:
        raise InvalidCookiePath
    return cookie


if __name__ == "__main__":
    c = getCookie("cookie.txt")
    print(c)

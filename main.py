# !/usr/bin/env python3

from imgur.imgur import Imgur
from tools import utils

if __name__ == "__main__":
    a = Imgur(cfgfile="./settings/auth.ini")
    # albdict = a.albums()
    # print(albdict)
    # imglist = a.get_images_from_album('boQrL')
    # print(imglist)
    utils.download(link='http://i.imgur.com/eSVGBik.jpg',
                   filename='eSVGBik.jpg')

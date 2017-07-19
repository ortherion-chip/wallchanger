# !/usr/bin/env python3

import urllib.request


def download(link=None, filename=None):
    '''
    Download file image
    '''

    if not filename or not link:
        print("Missing arguments")

    response = urllib.request.urlopen(link)

    meta = response.info()
    file_size = int(meta["Content-Length"])

    print("Downloading: {0} Bytes: {1}".format(filename, file_size))

    fobj = open(filename, 'wb')

    file_size_dl = 0
    block_sz = 2**16
    while True:
        buffer = response.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        fobj.write(buffer)

        print("Downloaded: {0} of {1}".format(file_size_dl, file_size))

    fobj.close()

#!/usr/bin/env python3

from imgurpython import ImgurClient
from configparser import ConfigParser
import urllib.request
import webbrowser


class Imgur(object):
    '''
    Class Imgur deals with authentication and download of images
    '''

    def __init__(self):
        self.authfile = 'auth.ini'
        self.authenticate()
        
    def get_credentials(self, imgurCli):
        # Authorization flow, pin example (see docs for other auth types)
        authorization_url = imgurCli.get_auth_url('pin')

        webbrowser.open(authorization_url, new=1)

        pin = input("Enter pin code: ")
        return imgurCli.authorize(pin, 'pin')
        
    def authenticate(self):
        '''
        Authentication on imgur server
        '''

        # Get client id and secret from config file auth.ini
        config = ConfigParser()
        config.read(self.authfile)
        client_id = config.get('credentials', 'client_id')
        client_secret = config.get('credentials', 'client_secret')

        client = ImgurClient(client_id, client_secret)
        
        try:
            client_access_token = config.get('credentials',
                                             'client_access_token')
            client_refresh_token = config.get('credentials',
                                              'client_refresh_token')
            # Case tokens are old
            client.set_user_auth(client_access_token, client_refresh_token)
        except:
            credentials = self.get_credentials(client)
            client_access_token = credentials['access_token']
            client_refresh_token = credentials['refresh_token']

            # Saving tokens on config file
            config.set('credentials', 'client_access_token',
                       client_access_token)
            config.set('credentials', 'client_refresh_token',
                       client_refresh_token)
            with open(self.authfile, 'w') as cfile:
                config.write(cfile)
                
            client.set_user_auth(client_access_token, client_refresh_token)

        print("Authentication successful! Here are the details:")
        # DEBUG
        # print("   Access token:  {0}".format(client_access_token))
        # print("   Refresh token: {0}".format(client_refresh_token))

        self.client = client

    def albums(self):
        '''
        Returns a dictionary with album_id as key and album_title as value
        '''

        album = {}
        for alb in self.client.get_account_albums('me'):
            album[alb.id] = alb.title
            # print("Album: {0} {1}".format(alb.title, alb.id))

        return album

    def get_images_from_album(self, albid):
        '''
        Get all images url from one album. Returns a dictionary with
        img_id as key and img_link as value
        '''
        
        img_dict = {}
        for img in self.client.get_album_images(albid):
            # img_dict.append(img.link)
            img_dict[img.id] = img.link
            
        return img_dict

    def get_image(self, imgid, imgname=None):
        '''
        Download image with imgid as imgname
        '''

        if not imgname:
            imgname = imgid
        
        url = self.client.get_image(imgid).link

        response = urllib.request.urlopen(url)

        meta = response.info()
        file_size = int(meta["Content-Length"])
        print(file_size)
        
        print("Downloading: {0} Bytes: {1}".format(imgname, file_size))

        imgf = open(imgname, 'wb')

        file_size_dl = 0
        block_sz = 2**16
        while True:
            buffer = response.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            imgf.write(buffer)

            print("Downloaded: {0} of {1}".format(file_size_dl, file_size))
            
        imgf.close()


if __name__ == "__main__":
    a = Imgur()
    albdict = a.albums()


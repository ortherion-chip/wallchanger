# !/usr/bin/env python3

from imgurpython import ImgurClient
from configparser import ConfigParser
import webbrowser


class Imgur(object):
    '''
    Class Imgur deals with authentication and download of images
    '''

    def __init__(self, cfgfile='auth.ini'):
        self.authfile = cfgfile
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
        Returns a list with album_id and album_title
        '''

        album = []
        for alb in self.client.get_account_albums('me'):
            item = {'id': alb.id, 'title': alb.title}
            album.append(item)
            # print("Album: {0} {1}".format(alb.title, alb.id))

        return album

    def get_images_from_album(self, albid):
        '''
        Get all images url from one album. Returns a dictionary with
        img_id as key and img_link as value
        '''

        img_dict = []
        for img in self.client.get_album_images(albid):
            item = {'id': img.id, 'link': img.link}
            img_dict.append(item)

        return img_dict

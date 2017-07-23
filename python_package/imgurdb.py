#!/usr/bin/env python3

from ..imgur.imgur import Imgur
from ..tools.sqlite import Sqlite, SqliteError
import random


class ImgurDB(object):
    '''
    Class to manipulate imgur database.
    '''

    table = "images"

    def __init__(self, dbpath, cfg):
        if not dbpath:
            raise TypeError("DB File cannot be instance of 'None'"
                            " Type")
        if not cfg:
            raise TypeError("Imgur settings file cannot be instance"
                            " of 'None' Type")

        try:
            self.db = Sqlite(dbpath)
        except:
            # Passing to parent the following Exceptions:
            # TypeError, PermissionError, FileNotFoundError
            raise

        self.imgur = Imgur(cfg)

    def close(self):
        '''
        Close connection to the database
        '''
        self.db.close()

    def create_table(self):
        '''
        Creates <table> for imgur server
        '''

        query = """
        CREATE TABLE {0} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imgur_id VARCHAR(50) NOT NULL,
        imgur_link VARCHAR(255) NOT NULL,
        imgur_album VACHAR(50) NOT NULL,
        used INT(1) DEFAULT 0
        );
        """.format(self.table)

        try:
            self.db.execute(query)
        except SqliteError as e:
            raise IOError("Sql execute error: {0}\n"
                          "query: {1}".format(e, query))
        except Warning as w:
            print("Warning: {}".format(w))

        self.db.commit()

    def insert(self, iid, ilink, ialbum):
        '''
        Insert images individually
        '''

        if not iid:
            raise TypeError("Imgur image id of 'None' type")
        if not ilink:
            raise TypeError("Imgur image link of 'None' type")
        if not ialbum:
            raise TypeError("Imgur image album of 'None' type")

        params = {'table': self.table,
                  'imgur_id': iid,
                  'imgur_link': ilink,
                  'imgur_album': ialbum,
                  'used': 0}
        query = """
        INSERT INTO {table}
        (imgur_id, imgur_link, imgur_album, used)
        VALUES
        ({imgur_id}, {imgur_link}, {imgur_album}, {used})
        """.format(params)

        try:
            self.db.execute(query)
        except SqliteError as e:
            raise IOError("Sql execute error: {0}\n"
                          "params: {1}\n"
                          "query: {2}".format(e, params, query))
        except Warning as w:
            print("Warning: {}".format(w))

        self.db.commit()

    def insert_by_album(self, album):
        '''
        Fetch all images from album and insert on database
        '''

        img_list = self.imgur.get_images_from_album(album)

        for img in img_list:
            try:
                self.insert(img['id'], img['link'], album)
            except:
                # Passing to parent the following Exceptions:
                # TypeError, IOError
                raise

    def update(self, cid, iid, ilink, ialbum, used):
        '''
        Insert images individually
        '''

        if not cid:
            raise TypeError("Image id on database of 'None' type")
        if not iid:
            raise TypeError("Imgur image id of 'None' type")
        if not ilink:
            raise TypeError("Imgur image link of 'None' type")
        if not ialbum:
            raise TypeError("Imgur image album of 'None' type")

        params = {'table': self.table,
                  'id': cid,
                  'imgur_id': iid,
                  'imgur_link': ilink,
                  'imgur_album': ialbum,
                  'used': 0}
        query = """
        UPDATE {table} SET
        imgur_id = {imgur_id},
        imgur_link = {imgur_link},
        imgur_album = {imgur_album},
        used = {used}
        WHERE
        id = {id}
        """.format(params)

        try:
            self.db.execute(query)
        except SqliteError as e:
            raise IOError("Sql execute error: {0}\n"
                          "params: {1}\n"
                          "query: {2}".format(e, params, query))
        except Warning as w:
            print("Warning: {}".format(w))

        self.db.commit()

    def get_random(self):
        '''
        Returns a dict with random row from database
        '''

        query1 = """
        SELECT count(*) AS cnt FROM {} WHERE USED = 0
        """.format(self.table)

        # Select command
        self.db.execute(query1)

        cnt = int(self.db.fetchone()['cnt'])

        sid = random.randrange(cnt)

        query2 = """
        SELECT * FROM {0} WHERE USED == 0
        LIMIT {1}, 1
        """.format(self.table, sid)

        # Select command
        self.db.execute(query2)

        return self.db.fetchone()

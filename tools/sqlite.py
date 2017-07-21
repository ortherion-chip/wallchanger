#!/usr/bin/env python3

import sqlite3


class QueryError(Exception):
    '''
    Exception raised errors in query.

    Attributes:
        expression -- input expression in which error occurred
        message -- explanation of error
    '''

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Sqlite(object):
    '''
    Class for sqlite3 interface.
    '''

    def __init__(self, db=None):

        try:
            f = open(db, 'r+')
        except TypeError:
            raise TypeError("Invalid file: {}".format(db))
        except PermissionError:
            raise PermissionError("Permission denied: {}".format(db))
        except FileNotFoundError:
            raise FileNotFoundError("File not found: {}".format(db))
        finally:
            f.close()

        self.conn = sqlite3.connect(db)

    def execute(self, query=None, params=None):
        '''
        Execute a query on sqlite3
        '''

        if not query:
            raise QueryError(query, "Empty query on execute function.")

        # params can be None
        cursor = self.conn.cursor()

        cursor.execute(query, params)

    def commit(self):
        '''
        Commit changes to the database
        '''
        self.conn.commit()

    def close(self):
        '''
        Close connection to the database
        '''
        self.conn.close()

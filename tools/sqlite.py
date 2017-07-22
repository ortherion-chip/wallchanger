#!/usr/bin/env python3

import sqlite3


class Error(Exception):
    '''
    Base class for exceptions
    '''
    pass


class SqliteError(Error):
    '''
    Exception raised errors in the class.

    Attributes:
        message -- explanation of error
        expression -- input expression in which error occurred
    '''

    def __init__(self, message, expression, *args):
        self.message = message
        self.expression = expression
        super(SqliteError, self).__init__(message, expression, *args)


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
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def commit(self):
        '''
        Commit changes to the database
        '''
        self.conn.commit()

    def close(self):
        '''
        Close connection to the database
        '''
        self.cursor.close()
        self.conn.close()

    def execute(self, query=None, params=None):
        '''
        Execute a query on sqlite3
        '''

        if not query:
            raise SqliteError("Empty query on execute function.",
                              query)

        # params can be None
        try:
            self.cursor.execute(query, params)
        except sqlite3.DataError as err:
            raise SqliteError("Data Error.", err)
        except sqlite3.IntegrityError as err:
            raise SqliteError("Integrity Error.", err)
        except sqlite3.ProgrammingError as err:
            raise SqliteError("Programming Error.", err)
        except sqlite3.Warning as warn:
            raise Warning("Sqlite Warning.", warn)
        except sqlite3.Error as err:
            raise SqliteError("Error.", err)

    def fetchone(self):
        '''
        sqlite3 fetchone wrapper
        '''
        return self.cursor.fetchone()

    def fetchall(self):
        '''
        sqlite3 fetchall wrapper
        '''
        return self.cursor.fetchall()

    def lastrowid(self):
        '''
        sqlite3 lastrowid wrapper
        '''
        return self.cursor.lastrowid

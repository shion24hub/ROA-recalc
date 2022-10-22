import os
import sqlite3
import os

class YetClosedError(Exception) :
    pass

class Database :

    """
    later.
    """

    def __init__(self, path : str) -> None:

        """
        later.
        """

        self.path = path
        self.nowConnect = False
    
    def connectCursor(self) -> None :

        """
        later.
        """
        
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        self.nowConnect = True
        self.connection = connection
        self.cursor = cursor
    
    def init(self) -> None :

        """
        later.
        """

        if self.nowConnect :
            error = "Connection to the database is not closed, use the finish method."
            raise YetClosedError(error)

        is_file = os.path.isfile(self.path)
        if is_file :
            os.remove(self.path)
        
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        sql = "create table info(name string, fins json, bs json)"
        cursor.execute(sql)

        connection.commit()
        connection.close()

    def finish(self) -> None :

        """
        later.
        """

        self.nowConnect = False
        self.connection.commit()
        self.connection.close()
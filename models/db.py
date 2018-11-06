import os
import sys
import psycopg2 as dbapi2
class Database:
    def __init__(self):
        print("self")
    def execute(self, sql, args):
        with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            self.cursor = cursor
            self.connection = connection
            return cursor
    def close(self):
        self.cursor.close()
        self.connection.close()
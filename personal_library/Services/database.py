from psycopg2 import pool


class Database:
    def __init__(self, user, host, password, db_name, port):
      self.user = user
      self.host = host
      self.password = password
      self.db_name = db_name
      self.port = port

    def connect(self):
      db_pool = pool.SimpleConnectionPool(
        host=self.host,
        database=self.db_name,
        user=self.user,
        password=self.password,
        port=self.port
      )
      conn = db_pool.getconn()
      self.conn = conn

    def check_connection(self):
       pass
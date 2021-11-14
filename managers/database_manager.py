# The below code is to directly talk to the db without using any ORM
import psycopg2
from psycopg2.extras import RealDictCursor

from managers.log_manager import LogManager


class DatabaseManager:
    def __init__(self):
        self.host = "127.0.0.1"
        self.username = "postgres"
        self.password = ""
        self.port = 5432
        self.dbname = "fastapi"
        self.conn = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def execute_query(self, query, query_data=(), single_record_flag=False):
        result = None
        cursor = None
        try:
            if self.conn is None:
                conn = psycopg2.connect(host=self.host,
                                        user=self.username,
                                        password=self.password,
                                        port=self.port,
                                        dbname=self.dbname,
                                        cursor_factory=RealDictCursor)
                LogManager().logger.info("Connected to the database successfully")
                self.conn = conn
            cursor = self.conn.cursor()
            cursor.execute(query, query_data)
            if single_record_flag:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            self.conn.commit()
        except psycopg2.DatabaseError as dbe:
            LogManager().logger.error(f"Connecting to db failed with error: {dbe}")
            raise dbe
        finally:
            return result

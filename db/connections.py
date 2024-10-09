import os

import psycopg2


class DatabaseManager:
    def __init__(self):
        self.DB_HOST = os.environ.get('DB_HOST')
        self.DB_NAME = os.environ.get('DB_NAME')
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')

    def get_db_connection(self):
        conn = psycopg2.connect(
            host=self.DB_HOST,
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASSWORD
        )
        return conn

    def execute_sql(self, query: str, params: tuple = None):
        conn = self.get_db_connection()
        cur = conn.cursor()

        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        if query.strip().lower().startswith('select'):
            result = cur.fetchall()
            cur.close()
            conn.close()
            return result

        conn.commit()
        cur.close()
        conn.close()

        return "SQL query executed successfully!"

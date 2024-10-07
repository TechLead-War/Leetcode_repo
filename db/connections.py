import psycopg2


class DatabaseManager:
    def __init__(self):
        self.DB_HOST = "localhost"
        self.DB_NAME = "gehu_leetcode"
        self.DB_USER = "postgres"
        self.DB_PASSWORD = "password"

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

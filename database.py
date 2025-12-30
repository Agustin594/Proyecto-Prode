from connection import get_connection

class Database:
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor(cursor_factory=None)

    def execute(self, sql, params=None):
        self.cur.execute(sql, params)
        self.conn.commit()

    def fetch_one(self, sql, params=None):
        self.cur.execute(sql, params)
        return self.cur.fetchone()

    def fetch_all(self, sql, params=None):
        self.cur.execute(sql, params)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
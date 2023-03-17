import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def query_db(self, query, args=(), one=False):
        self.cursor.execute(query, args)
        r = [dict((self.cursor.description[i][0], value) \
                  for i, value in enumerate(row)) for row in self.cursor.fetchall()]
        return (r[0] if r else None) if one else r

    def get_all(self, typ: str):
        try:
            data = self.query_db(f"select * from {typ}")
            return data
        except Exception as e:
            return f"ERROR | {e}"

    def search(self, query: str, typ: str):
        try:
            data = self.query_db(f"SELECT * FROM {typ} WHERE NAME LIKE '%'||?||'%'", (query,))
            return data
        except Exception as e:
            return f"ERROR | {e}"

    def insert(self, name: str, ingredients: str, price: str, typ: str):
        try:
            if name and ingredients and not price:
                self.cursor.execute(f"INSERT INTO {typ} (NAME, INGREDIENTS) \
                        VALUES (?,?)", (name, ingredients))
                self.conn.commit()
                return "Success"
            elif name and price and not ingredients:
                self.cursor.execute(f"INSERT INTO {typ} (NAME, Price) \
                            VALUES (?,?)", (name, price))
                self.conn.commit()
                return "Success"
            else:
                return f"ERROR | Given parameters are not complete"
        except Exception as e:
            return f"ERROR | {e}"

    def delete_by_id(self, ID: int, typ: str):
        self.cursor.execute(f"DELETE FROM {typ} WHERE id = {ID}")
        self.conn.commit()

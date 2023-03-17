import json
import sqlite3
from flask import Flask, request

app = Flask(__name__)


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


db = Database()


@app.route('/<typ>')
def pizza(typ):
    typ = typ.capitalize()
    return json.dumps(db.get_all(typ=typ))


@app.route('/<typ>/add', methods=['POST'])
def pizza_add(typ):
    typ = typ.capitalize()
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            ingredients = request.form.get('ingredients')
            price = request.form.get('price')
            response = db.insert(typ=typ, name=name, ingredients=ingredients, price=price)
            if 'ERROR' in response:
                return json.dumps({'success': False, 'ERROR': f'{response}'}), 200, {'ContentType': 'application/json'}
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except Exception as e:
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


@app.route('/<typ>/delete', methods=['POST'])
def pizza_delete(typ):
    typ = typ.capitalize()
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            db.delete_by_id(ID=id, typ=typ)
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except Exception as e:
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


@app.route('/<typ>/search', methods=['POST'])
def pizza_search(typ: str):
    typ = typ.capitalize()
    if request.method == 'POST':
        try:
            query = request.form.get('query')
            return json.dumps(db.search(query=query, typ=typ))
        except Exception as e:
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


app.run(debug=False)

import json
import sqlite3
from flask import Flask, request

app = Flask(__name__)

conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
print("Opened database successfully")


def get_all(typ: str):
    try:
        cursor.execute(f"select * from {typ}")
        data = cursor.fetchall()
        return data
    except Exception as e:
        return f"ERROR | {e}"


def search(query: str, typ: str):
    try:
        cursor.execute(f"SELECT * FROM {typ} WHERE NAME LIKE '%'||?||'%'", (query,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        return f"ERROR | {e}"


def insert(name: str, ingredients: str, price: str, typ: str):
    try:
        if name and ingredients and not price:
            cursor.execute(f"INSERT INTO {typ} (NAME, INGREDIENTS) \
                    VALUES (?,?)", (name, ingredients))
            conn.commit()
        elif name and price and not ingredients:
            cursor.execute(f"INSERT INTO Cenik (NAME, INGREDIENTS) \
                        VALUES (?,?)", (name, ingredients))
            conn.commit()
        else:
            return f"ERROR | Given parameters are not complete"
    except Exception as e:
        return f"ERROR | {e}"


def delete_by_id(ID: int, typ: str):
    cursor.execute(f"DELETE FROM {typ} WHERE id = {ID}")
    conn.commit()


@app.route('/<typ>')
def pizza(typ):
    typ = typ.capitalize()
    return json.dumps(get_all(typ))


@app.route('/<typ>/add', methods=['POST'])
def pizza_add(typ):
    typ = typ.capitalize()
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            ingredients = request.form.get('ingredients')
            price = request.form.get('price')
            insert(typ=typ, name=name, ingredients=ingredients, price=price)
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except Exception as e:
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


@app.route('/<typ>/delete', methods=['POST'])
def pizza_delete(typ):
    typ = typ.capitalize()
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            delete_by_id(ID=id, typ=typ)
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except Exception as e:
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


@app.route('/<typ>/search', methods=['POST'])
def pizza_search(typ: str):
    typ = typ.capitalize()
    if request.method == 'POST':
        try:
            query = request.form.get('query')
            return json.dumps(search(query, typ=typ))
        except Exception as e:
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


app.run(debug=False)

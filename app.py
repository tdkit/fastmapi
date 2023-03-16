import json
import sqlite3
from flask import Flask, request

app = Flask(__name__)

conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
print("Opened database successfully")


def get_all(typ: str):
    cursor.execute(f"select * from {typ}")
    data = cursor.fetchall()
    return data


def search(query: str, typ: str):
    cursor.execute(f"SELECT * FROM {typ} WHERE NAME LIKE '%'||?||'%'", (query,))
    data = cursor.fetchall()
    return data


def pizza_insert(name: str, ingredients: str):
    cursor.execute(f"INSERT INTO Pizza (NAME, INGREDIENTS) \
            VALUES (?,?)", (name, ingredients))
    conn.commit()


def delete_by_id(id: int, typ: str):
    cursor.execute(f"DELETE FROM {typ} WHERE id = {id}")
    conn.commit()


@app.route('/<typ>')
def pizza(typ):
    return json.dumps(get_all(typ))


@app.route('/pizza/add', methods=['POST'])
def pizza_add():
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        pizza_insert(name, ingredients)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/pizza/delete', methods=['POST'])
def pizza_delete():
    if request.method == 'POST':
        id = request.form.get('id')
        delete_by_id(id=id, typ="Pizza")
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/pizza/search', methods=['POST'])
def pizza_search():
    if request.method == 'POST':
        query = request.form.get('query')
        return json.dumps(search(query, typ='Pizza'))


app.run(host="localhost")

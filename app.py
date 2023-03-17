import json
from flask import Flask, request
from database import Database

app = Flask(__name__)  # Initializing flask app

db = Database()  # Initializing database class imported from file database.py


@app.route('/<typ>')  # GET request with available types: Pizza, Napoje, Deserty, Cenik (All of these also work below)
def pizza(typ):
    typ = typ.capitalize()
    return json.dumps(db.get_all(typ=typ))


@app.route('/<typ>/add', methods=['POST'])  # POST request with Body structure as form-data. Keys: name, ingredients
def pizza_add(typ):

    typ = typ.capitalize()  # Clunky way of getting database table name ("typ" variable)

    if request.method == 'POST':
        try:
            # Parsing data from form-data body
            name = request.form.get('name')
            ingredients = request.form.get('ingredients')
            price = request.form.get('price')

            # Inserting into database
            response = db.insert(typ=typ, name=name, ingredients=ingredients, price=price)

            if 'ERROR' in response:  # Detecting if database function succeeded

                # Error message
                return json.dumps({'success': False, 'ERROR': f'{response}'}), 200, {'ContentType': 'application/json'}

            # Success message
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

        except Exception as e:

            # Error message
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


@app.route('/<typ>/delete', methods=['POST'])  # POST request with Body structure as form-data. Keys: id
def pizza_delete(typ):

    typ = typ.capitalize()  # Clunky way of getting database table name ("typ" variable)

    if request.method == 'POST':
        try:
            # Parsing data from form-data body
            item_id = request.form.get('id')

            # Deleting item with matching item_id from database
            db.delete_by_id(ID=item_id, typ=typ)

            # Success message
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

        except Exception as e:

            # Error message
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


@app.route('/<typ>/search', methods=['POST'])  # POST request with Body structure as form-data. Keys: query
def pizza_search(typ: str):

    typ = typ.capitalize()  # Clunky way of getting database table name ("typ" variable)

    if request.method == 'POST':
        try:
            # Parsing data from form-data body
            query = request.form.get('query')

            # Getting and returning data parsed from database if query is in NAME value of item
            return json.dumps(db.search(query=query, typ=typ))

        except Exception as e:

            # Error message
            return json.dumps({'success': False, 'ERROR': f'{e}'}), 200, {'ContentType': 'application/json'}


# app.run()  # Initializing flask app for debugging

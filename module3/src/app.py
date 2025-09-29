import os

from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from db import db
from coffee import Coffee

DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///:memory:'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.app_context().push()
db.init_app(app)


@app.route("/coffees", methods=["GET"])
def get_coffees():
    try:
        coffees = [coffee.json for coffee in Coffee.find_all()]
        return jsonify(coffees)
    # except Exception as e:
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route("/coffee/<int:coffee_id>", methods=["GET"])
def get_coffee(coffee_id):
    try:
        coffee = Coffee.find_by_id(coffee_id)
        if coffee:
            return jsonify(coffee.json), {'Content-Type': 'application/json',
                                          'Location': f'/coffee/{coffee.id}',
                                          'ETag': f'{coffee.version}'}
        return jsonify({'error': f'Coffee {id} not found'}), 404
    # except Exception as e:
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route("/coffee", methods=["POST"])
def create_coffee():
    request_data = request.get_json()
    if 'name' not in request_data or request_data['name'] is None or request_data['name'] == '':
        return jsonify({"error": "Missing name"}), 400

    try:
        coffee = Coffee(None, name=request_data['name'], version=1)
        coffee.save()
        return jsonify(coffee.json), 201, {'Content-Type': 'application/json',
                                           'Location': f'/coffee/{coffee.id}',
                                           'ETag': f'{coffee.version}'}
    # except Exception as e:
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@app.route("/coffee/<int:coffee_id>", methods=["PUT"])
def update_coffee(coffee_id):
    # Get the request data
    request_data = request.get_json()
    if_match_header = int(request.headers.get('If-Match'))

    # Validate fields
    if not request_data.get('name'):
        return jsonify({"error": "Missing name"}), 400

    # Find the coffee we want to update
    coffee = Coffee.find_by_id(coffee_id)
    if coffee is None:
        # We did not find the coffee
        return jsonify({"error": f"No coffee found with ID {id}"}), 404

    # Validate the version
    if if_match_header != coffee.version:
        return jsonify(
            {
                "error": f"Version conflict for coffee with ID {id}: version = {coffee.version}, "
                         f"If-Match = {if_match_header}"
            }
        ), 409

    # Update the name of the coffee
    coffee.name = request_data['name']

    # Increment the coffee's version
    coffee.version = coffee.version + 1

    # Update the coffee in the database
    coffee.save()

    # Return the updated coffee
    return jsonify(coffee.json), 200, {'Content-Type': 'application/json',
                                  'Location': f'/coffee/{coffee.id}',
                                  'ETag': f'{coffee.version}'}

@app.route("/coffee/<int:coffee_id>", methods=["DELETE"])
def delete_coffee(coffee_id):
    coffee = Coffee.find_by_id(coffee_id)
    if coffee is None:
        return jsonify({"error": f"No coffee found with ID {id}"}), 404

    coffee.delete()
    return f'Deleted coffee {id}'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

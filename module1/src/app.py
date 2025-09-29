from flask import Flask, jsonify, request

app = Flask(__name__)

COFFEES = [
    {"id": 1, "name": "Coffee 1", "version": 1},
    {"id": 2, "name": "Coffee 2", "version": 1},
    {"id": 3, "name": "Coffee 3", "version": 1},
]


@app.route("/coffees", methods=["GET"])
def get_coffees():
    return jsonify(COFFEES)


@app.route("/coffee/<int:id>", methods=["GET"])
def get_coffee(id):
    coffee_list = [c for c in COFFEES if c['id'] == id]
    if len(coffee_list) == 0:
        return jsonify({"error": "No such coffee found"}), 404

    coffee = coffee_list[0]
    return jsonify(coffee), {'Content-Type': 'application/json',
                             'Location': f'/coffee/{coffee["id"]}',
                             'ETag': f'{coffee["version"]}'}


@app.route("/coffee", methods=["POST"])
def create_coffee():
    request_data = request.get_json()
    if not request_data['name']:
        return jsonify({"error": "Missing name"}), 400

    # Compute the new id
    new_id = max([c['id'] for c in COFFEES]) + 1

    # Add the coffee to our list
    new_coffee = {
        "id": new_id,
        "name": request_data['name'],
        "version": 1
    }
    COFFEES.append(new_coffee)

    return jsonify(new_coffee), 201, {'Content-Type': 'application/json',
                             'Location': f'/coffee/{new_coffee["id"]}',
                             'ETag': f'{new_coffee["version"]}'}


@app.route("/coffee/<int:id>", methods=["PUT"])
def update_coffee(id):
    # Get the request data
    request_data = request.get_json()
    if 'If-Match' not in request.headers:
        return jsonify({"error": "If-Match header is required"}), 400

    if_match_header = int(request.headers.get('If-Match'))

    # Validate fields
    if not request_data.get('name'):
        return jsonify({"error": "Missing name"}), 400

    # Find the coffee we want to update
    for coffee in COFFEES:
        if coffee['id'] == id:
            # Validate the version
            if if_match_header != coffee['version']:
                return jsonify(
                    {"error": f"Version conflict for coffee with ID {id}: version = {coffee['version']}, If-Match = {if_match_header}"}), 409

            # Update the name of the coffee
            coffee['name'] = request_data['name']

            # Increment the coffee's version
            coffee['version'] = coffee['version'] + 1

            # Return the updated coffee
            return jsonify(coffee), 200, {'Content-Type': 'application/json',
                             'Location': f'/coffee/{coffee["id"]}',
                             'ETag': f'{coffee["version"]}'}

    # We did not find the coffee
    return jsonify({"error": f"No coffee found with ID {id}"}), 404


@app.route("/coffee/<int:id>", methods=["DELETE"])
def delete_coffee(id):
    coffee_list = [c for c in COFFEES if c['id'] == id]
    if len(coffee_list) == 1:
        COFFEES.remove(coffee_list[0])
        return f'Deleted coffee {id}'
    return jsonify({"error": f"No coffee found with ID {id}"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

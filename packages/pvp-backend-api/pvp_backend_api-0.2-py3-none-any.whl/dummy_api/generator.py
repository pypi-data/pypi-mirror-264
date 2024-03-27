import os

def generate_template(output_path):
    # Generate basic structure
    template = """
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data (replace with your own data structure)
data = {}

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/data/<id>', methods=['GET'])
def get_single_data(id):
    return jsonify(data.get(id))

@app.route('/data', methods=['POST'])
def create_data():
    new_data = request.json
    data[new_data['id']] = new_data
    return jsonify(new_data), 201

@app.route('/data/<id>', methods=['PUT'])
def update_data(id):
    if id not in data:
        return jsonify({'error': 'Not found'}), 404
    updated_data = request.json
    data[id] = updated_data
    return jsonify(updated_data)

@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    if id not in data:
        return jsonify({'error': 'Not found'}), 404
    del data[id]
    return jsonify({'message': 'Deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
"""

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Write template to the specified path
    output_file = os.path.join(output_path, "template.py")
    with open(output_file, "w") as file:
        file.write(template)

    print(f"PVP API template generated at: {output_file}")
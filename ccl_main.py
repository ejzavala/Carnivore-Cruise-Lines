#basic API start
from flask import Flask, jsonify, abort
from cruiseItem import cruiseItem


app = Flask(__name__)
app.json_encoder.default = lambda self, o: o.to_joson()

# Array to store the objects
InventoryArr = {}

@app.route('/inventory', methods=['GET'])

@app.route('/inventory/location/< location >', methods=['GET'])


if __name__ == '__main__':
    app.run("0.0.0.0", 80)
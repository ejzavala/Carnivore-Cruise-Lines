#basic API start
from flask import Flask, jsonify, abort
from cruiseItem import cruiseItem


app = Flask(__name__)
app.json_encoder.default = lambda self, o: o.to_joson()

# Array to store the objects
InventoryArr = {};

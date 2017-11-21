#basic API start
from flask import Flask, jsonify, abort
from cruiseItem import cruiseItem
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine(database path goes here)
app = Flask(__name__)
app.json_encoder.default = lambda self, o: o.to_joson()
api = Api(app)

# Array to store the objects
InventoryArr = {}

def get_cruiseitemArr():
    conn = db_connect.connect() # connect to database
    InventoryArr = conn.execute("select * from CruiseItem") #Perform query for all CruiseItems in db
    return jsonify(InventoryArr) #converts query result into a json using jsonify

def get_cruiseitemArr_byLoc(fromLocation):
    conn = db_connect.connect() #connect to database
    query = conn.execute("select * from CruiseItem where fromLocation =%s "%string(fromLocation))
    return jsonify(query) #convert query result into a json

@app.route('/inventory', methods=['GET'])
def get_cruiseitems():
    return jsonify(status="ok",InventoryArr=InventoryArr)


@app.route('/inventory/location/< location >', methods=['GET'])
def get_cruiseitems_by_location(location):
    return jsonify(status="ok", InventoryArr=get_cruiseitems_by_location(location))


if __name__ == '__main__':
    app.run("0.0.0.0", 80)
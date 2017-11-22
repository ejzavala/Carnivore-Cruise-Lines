#basic API start
from flask import Flask, jsonify, abort, request
from cruiseItem import cruiseItem
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///Carnivorecruise.sqlite')
app = Flask(__name__)
app.json_encoder.default = lambda self, o: o.to_joson()
app.app_context()

# Array to store the objects
InventoryArr = {}

def get_cruiseitemArr():
    conn = db_connect.connect() # connect to database
    query = conn.execute("select * from CruiseItem") #Perform query for all CruiseItems in db
    InventoryArr = query.cursor.fetchall()
    query = conn.execute("select itemID, cruiseLinerID, roomID, available, cost, name, description, roomCapacity, fromLocation, departureDate, returnDate, duration from cruiseItem;")
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

def get_cruiseitemArr_byLoc(Location):
    conn = db_connect.connect() #connect to database
    query = conn.execute("select * from Cruiseitem where fromLocation ='%s'"%str(Location))
    InventoryArr = query.cursor.fetchall()
    query = conn.execute("select itemID, cruiseLinerID, roomID, available, cost, name, description, roomCapacity, fromLocation, departureDate, returnDate, duration from cruiseItem where fromLocation ='%s';"%str(Location))
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    #print(InventoryArr)
    return jsonify(result) #convert query result into a json

@app.route('/inventory', methods=['GET'])
def get_cruiseitems():
    return jsonify(status="ok",InventoryArr=get_cruiseitemArr())

#example call would be get_cruiseitems_by_location('Starkville', 'MS')
@app.route('/inventory/location/<state>/<city>', methods=['GET'])
def get_cruiseitems_by_location(city, state):
    loc_and_state = str(city + ',' + ' ' + state)
    print (loc_and_state)
    return jsonify(status="ok", InventoryArr=get_cruiseitemArr_byLoc(loc_and_state))


if __name__ == '__main__':
    app.run("0.0.0.0", 80)

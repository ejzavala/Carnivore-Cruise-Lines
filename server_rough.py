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
HistoryArr = {}

def get_cruiseitemArr():
    conn = db_connect.connect() # connect to database
    query = conn.execute("select * from CruiseItem") #Perform query for all CruiseItems in db
    InventoryArr = query.cursor.fetchall()
    print(InventoryArr)
    return jsonify(InventoryArr)

def get_cruiseitemArr_byLoc(Location):
    conn = db_connect.connect() #connect to database
    query = conn.execute("select * from Cruiseitem where fromLocation ='%s'"%str(Location))
    InventoryArr = query.cursor.fetchall()
    print(InventoryArr)
    return jsonify(query) #convert query result into a json

def get_cruiseHistory():
    conn = db_connect.connect() # connect to database
    query = conn.execute("select * from cruiseHistory")
    HistoryArr = query.cursor.fetchall()
    print(HistoryArr)

@app.route('/inventory', methods=['GET'])
def get_cruiseitems():
    return jsonify(status="ok",InventoryArr=get_cruiseitemArr())


@app.route('/inventory/location/<Location>', methods=['GET'])
def get_cruiseitems_by_location(Location):
    return jsonify(status="ok", InventoryArr=get_cruiseitemArr_byLoc(Location))


if __name__ == '__main__':
    app.run("0.0.0.0", 80)

from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from cruiseItem import cruiseItem
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///Carnivorecruise.sqlite')
app = Flask(__name__)
CORS(app)
app.json_encoder.default = lambda self, o: o.to_json()
app.app_context()

# Array to store the objects
InventoryArr = {}
HistoryArr = {}

def get_cruiseitemArr():
    conn = db_connect.connect() # connect to database
    query = conn.execute("select * from CruiseItem") #Perform query for all CruiseItems in db
    InventoryArr = query.cursor.fetchall()
    query = conn.execute("select itemID, cruiseLinerID, roomID, available, cost, name, description, roomCapacity, fromLocation, departureDate, returnDate, duration from cruiseItem;")
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return result

def get_cruiseitemArr_byLoc(Location):
    conn = db_connect.connect() #connect to database
    query = conn.execute("select * from Cruiseitem where fromLocation ='%s'"%str(Location))
    InventoryArr = query.cursor.fetchall()
    query = conn.execute("select itemID, cruiseLinerID, roomID, available, cost, name, description, roomCapacity, fromLocation, departureDate, returnDate, duration from cruiseItem where fromLocation ='%s';"%str(Location))
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    #print(InventoryArr)
    return result #convert query result into a json

def get_cruiseHistory():
    conn = db_connect.connect() # connect to database
    query = conn.execute("select * from cruiseHistory")
    HistoryArr = query.cursor.fetchall()
    query = conn.execute("select itemID, numberSold from cruiseHistory;")
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return result

def add_to_history(cruise_item_idnum):
    conn = db_connect.connect()
    queryhistory = conn.execute("SELECT numberSold FROM cruiseHistory WHERE itemID = '%s'"%(cruise_item_idnum))
    numberactuallysold = queryhistory.cursor.fetchall()
    if len(numberactuallysold) != 0:
        sold = numberactuallysold[0][0]
        sold = (sold + 1)
        query = conn.execute("UPDATE cruiseHistory SET numberSold = (?) WHERE itemID = (?)",(sold, cruise_item_idnum))
    else:
        query = conn.execute("INSERT INTO cruiseHistory (itemID, numberSold) VALUES ('%s', 1)" %str(cruise_item_idnum))

#changes cruiseItem Table
def put_changeAvail(cruise_item_id):
    conn = db_connect.connect()
    query = conn.execute("SELECT ItemID FROM cruiseItem WHERE itemID = '%s'"%(cruise_item_id))
    if (len(query.cursor.fetchall()) != 0):
        checkQuery = conn.execute("SELECT available FROM cruiseItem WHERE itemID = '%s'"%(cruise_item_id))
        curAvail = checkQuery.cursor.fetchall()
        if curAvail[0][0] == 0:
            return False
        else:
            query = conn.execute("UPDATE cruiseItem SET available = 0 WHERE itemID = '%s'"%str(cruise_item_id))
            return True
    else:
        return False

@app.route('/system/purchase/<item_id>', methods=['PUT'])
def put_change_avail_api(item_id):
    if (put_changeAvail(item_id) == False):
        return jsonify(status="Item you tried to purchase an unavailable item")
    else:
        add_to_history(item_id)
        return jsonify (status="Item successfully purchased")

@app.route('/inventory', methods=['GET'])
def get_cruiseitems():
    return jsonify(status="ok",InventoryArr=get_cruiseitemArr())

#example call would be get_cruiseitems_by_location('Starkville', 'MS')
@app.route('/inventory/location/<state>/<city>', methods=['GET'])
def get_cruiseitems_by_location(city, state):
    loc_and_state = str(city + ',' + ' ' + state)
    print (loc_and_state)
    return jsonify(status="ok", InventoryArr=get_cruiseitemArr_byLoc(loc_and_state))

@app.route('/system/history', methods=['GET'])
def get_cruisehistory():
    return jsonify(status="ok", HistoryArr = get_cruiseHistory())

@app.route('/inventory/new/<itemID>/<linerID>/<roomID>/<availablity>/<cost>/<name>/<description>/<roomCapacity>/<fromLocation>/<departureDate>/<returnDate>/<duration>', methods=['POST'])
def insertInventory(itemID, linerID, roomID, availablity, cost, name, description, roomCapacity, fromLocation, departureDate, returnDate, duration):
    conn = db_connect.connect()
    checkQuery = conn.execute("SELECT ItemID FROM cruiseItem WHERE itemID = '%s'"%(itemID))
    test = checkQuery.cursor.fetchall()
    if len(test) != 0:
        return jsonify(status = "failed to add")
    else:
        query = conn.execute("INSERT INTO cruiseItem (itemID, cruiseLinerID, roomID, available, cost, name, description, roomCapacity, fromLocation, departureDate, returnDate, duration) VALUES (?,?,?,?,?,?,?,?, ?,?,?,?)", (itemID, linerID, roomID, availablity, cost, name, description, roomCapacity, fromLocation, departureDate, returnDate, duration))
        return jsonify(status="added")

@app.route('/inventory/<itemID>', methods=['DELETE'])
def deleteInventoryItem(itemID):
    conn= db_connect.connect()
    query = conn.execute("DELETE FROM cruiseItem WHERE itemID = (?)", (itemID))
    return jsonify(status = "Deleted")

@app.route('/inventory/<itemID>/<availablity>', methods=['PUT'])
def updateAvailablity(itemID, availablity):
    conn=db_connect.connect()
    checkQuery = conn.execute("SELECT ItemID FROM cruiseItem WHERE itemID = '%s'" % (itemID))
    test = checkQuery.cursor.fetchall()
    if len(test) != 0:
        query=conn.execute("UPDATE cruiseItem SET available = (?) WHERE itemID = '%s'"%str(itemID), (availablity))
        return jsonify(status="updated")
    else:
        return jsonify(status="No target")

if __name__ == '__main__':
    app.run("0.0.0.0", 80)
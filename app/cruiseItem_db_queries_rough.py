#Python class for CruiseItem
# itemID*	string($cruiseLinerID-roomID)
# example: MexicoAdventure-25
# cruiseLinerID*	string($shipName)
# example: Mexico Adventure
# roomID*	integer($int32)
# example: 25
# avalible*	boolean
# price*	integer($int32)
# example: 11395 => $113.95
# name*	string
# example: Mexico Adventure Suite
# description*	string
# example: Lovely port side suite on the Mexico Adventure Cruise Liner
# roomCapacity*	integer($int32)
# example: 6
# fromLocation*	string
# example: Tampa, FL
# departureDate*	string($YYYY-MM-DDTHH:mm:ss)
# example: OrderedMap {}
# returnDate*	string($YYYY-MM-DDTHH:mm:ss)
# example: OrderedMap {}
# duration*	integer($int32)
# example: 4
# }
db_connect = create_engine(database path goes here)
app = Flask(__name__)
api = Api(app)


class CruiseItems(Resource):
	def get(self):
		conn = db_connect.connect() # connect to database
		query = conn.execute("select * from CruiseItem") #Perform query for all CruiseItems in db
		return jsonify(query) #converts query result into a json using jsonify
	
class Locations(Resource)
	def get(self, fromLocation):
		conn = db_connect.connect() #connect to database
		query = conn.execute("select * from CruiseItem where fromLocation =%s "%string(fromLocation))
		return jsonify(query) #convert query result into a json

api.add_resource(CruiseItems, '/CruiseItems') # Route_1 show all cruise items
api.add_resource(fromLocation, '/CruiseItems/<fromLocation>') # Route_2	show all cruise items by location	

if __name__ == '__main__':
	app.run(port = '5002')
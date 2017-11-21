class cruiseItem:
    def __init__(self, inID, inLiner, inRoom, inAvalible, cost, inName, inDescription, inCapacity, inFromLocation, inDepartureDate, inReturnDate, inDuration):
        self.itemID = inID;
        self.cruiseLinerID = inLiner;
        self.roomID = inRoom;
        self.avalible = inAvalible;
        self.price = cost;
        self.name = inName;
        self.description = inDescription;
        self.roomCapacity = inCapacity;
        self.fromLocation = inFromLocation;
        self.departureDate = inDepartureDate;
        self.returnDate = inReturnDate;
        self.duration = inDuration;

    def update_Avalibity(self, inAvalible):
        self.avalible = inAvalible;

    def to_json(self):
        return {
            'item_id':self.itemID,
            'cruise_liner_id':self.cruiseLinerID,
            'room_id':self.roomID,
            'avalible':self.avalible,
            'cost':self.price,
            'name':self.name,
            'descrtipion':self.description,
            'room_capacity':self.roomCapacity,
            'from_location':self.fromLocation,
            'departure_date':self.departureDate,
            'return_date':self.returnDate,
            'duration':self.duration,
        }
    
class historyItem:
    def __init__(self, inID, inAmount):
        self.itemID = inID;
        self.numberSold = inAmount;

    def to_json(self):
        return {
            'item_ID':self.itemID,
            'number_of_item_sold':self.numberSold
}

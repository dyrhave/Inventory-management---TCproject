import json

with open('inventory.json') as json_data:
    inventory = json.load(json_data)

class Inventory:
    def __init__(self, id, brand, name, price, quantity):
        self.id = id
        self.brand = brand
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    @classmethod
    def create(cls, brand, name, price , quantity):
        ##Kode her##

    @classmethod
    def get(cls, id):
        ##Kode her##

    @classmethod
    def update(cls, brand, name, price , quantity):
        ##Kode her##

    @classmethod
    def delete(cls, id):
        ##Kode her##

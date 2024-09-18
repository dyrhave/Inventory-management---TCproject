import json

# Lager
class Inventory:
    _next_id = 1

    def __init__(self, brand, name, price, quantity, inv_id=None):
        self.inv_id = inv_id if inv_id is not None else self._get_next_id()
        self.brand = brand
        self.name = name
        self.price = price
        self.quantity = quantity

    @classmethod
    def _get_next_id(cls):
        current_id = cls._next_id
        cls._next_id += 1
        return current_id

    @classmethod
    def load_from_file(cls):
        try:
            with open('../data/inventory.json', 'r') as f:
                inventory = json.load(f)
            if inventory:
                cls._next_id = max(item['inv_id'] for item in inventory) + 1
                return inventory
        except FileNotFoundError:
            return []

    @classmethod
    def save_to_file(cls, inventory):
        with open('../data/inventory.json', 'w') as f:
            json.dump(inventory, f, indent=2)

    def to_dict(self):
        return {
            "inv_id": self.inv_id,
            "brand": self.brand,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    @classmethod
    def create(cls, brand, name, price , quantity):
        new_item = cls(brand, name, price, quantity)
        inventory = cls.load_from_file()
        inventory.append(new_item.to_dict())
        cls.save_to_file(inventory)
        return new_item

    @classmethod
    def get(cls, inv_id):
        inventory = cls.load_from_file()
        for item in inventory:
            if item['inv_id'] == inv_id:
                return cls(**item)
            return None

    @classmethod
    def update(cls, inv_id, **kwargs):
        inventory = cls.load_from_file()
        for item in inventory:
            if inv_id == item['inv_id']:
                item.update(**kwargs)
                cls.save_to_file(inventory)
                return item(**item)
        return None

    @classmethod
    def delete(cls, inv_id):
        inventory = cls.load_from_file()
        initial_inv = len(inventory)

        inventory = [item for item in inventory if item['inv_id'] != inv_id]
        if len(inventory) < initial_inv:
            cls.save_to_file(inventory)
            return True
        else:
            return False

    @classmethod
    def get_all(cls, inventory):
        return [cls(**item) for item in inventory]
import json

# Hent kundedata fra json
with open('../data/customers.json', 'r') as f:
    customers = json.load(f)

# Kunde
class Customer:
    def __init__(self, id, name, email, passwordHash):
        self.id = id
        self.name = name
        self.email = email
        self.passwordHash = passwordHash

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "passwordHash": self.passwordHash
        }

    @classmethod
    def create(cls, name, email, passwordHash):
        ##kode her##

    @classmethod
    def get(cls, id):
        ##kode her##


    @classmethod
    def update(cls, name, email, passwordHash):
        ##kode her##


    @classmethod
    def delete(cls, id):
        ##kode her##




customer = Customer("C004", "John Doe", "<EMAIL>", "<PASSWORD>" )
customer.to_dict()
print(customer.to_dict())
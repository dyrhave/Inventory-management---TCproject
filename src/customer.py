import json

# Kunde
class Customer:
    _next_id = 1

    def __init__(self, name, email, passwordHash, cust_id=None):
        self.cust_id = cust_id
        self.name = name
        self.email = email
        self.passwordHash = passwordHash

    @classmethod
    def _get_next_id(cls):
        current_id = cls._next_id
        cls._next_id += 1
        return current_id

    @classmethod
    def load_from_file(cls):
        try:
            with open('customers.json', 'r') as f:
                customers = json.load(f)
            if customers:
                cls._next_id = max(customer['inv_id'] for customer in customers) + 1
                return customers
        except FileNotFoundError:
            return []

    @classmethod
    def save_to_file(cls, customers):
        with open('customers.json', 'w') as f:
            json.dump(customers, f, indent=2)

    def to_dict(self):
        return {
            "cust_id": self.cust_id,
            "name": self.name,
            "email": self.email,
            "passwordHash": self.passwordHash
        }

    @classmethod
    def create(cls, name, email, passwordHash):
        new_customer = cls(name, email, passwordHash)
        customers = cls.load_from_file()
        customers.append(new_customer.to_dict())
        cls.save_to_file(customers)
        return new_customer

    @classmethod
    def get(cls, id):
        customers = cls.load_from_file()
        for customer in customers:
            if customer['id'] == id:
                return cls(**customer)
            return None

    @classmethod
    def update(cls, cust_id, **kwargs):
        customers = cls.load_from_file()
        for customer in customers:
            if customer['cust_id'] == cust_id:
                customer.update(**kwargs)
                cls.save_to_file(customers)
                return customer
        return None

    @classmethod
    def delete(cls, cust_id):
        customers = cls.load_from_file()
        initial_customers = len(customers)

        customers = [customer for customer in customers if customer['cust_id'] == cust_id]
        if len(customers) < initial_customers:
            cls.save_to_file(customers)
            return True
        else:
            return False

    @classmethod
    def get_all(cls, customers):
        return [cls(**customer) for customer in customers]
from app import app, db, User, Customer, Inventory, Order, OrderItem
from datetime import datetime, timedelta
import random

def populate_db():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create users
        users = [
            User(username="admin"),
            User(username="staff1"),
            User(username="staff2")
        ]
        for user in users:
            user.set_password("password123")
            db.session.add(user)

        # Create customers
        customers = [
            Customer(name="Alice Johnson", email="alice@example.com"),
            Customer(name="Bob Smith", email="bob@example.com"),
            Customer(name="Charlie Brown", email="charlie@example.com")
        ]
        db.session.add_all(customers)

        # Create inventory items
        items = [
            Inventory(name="Laptop", price=999.99, quantity=50),
            Inventory(name="Mouse", price=29.99, quantity=100),
            Inventory(name="Keyboard", price=59.99, quantity=75),
            Inventory(name="Monitor", price=199.99, quantity=30)
        ]
        db.session.add_all(items)

        # Commit to get IDs
        db.session.commit()

        # Create orders
        for _ in range(20):
            customer = random.choice(customers)
            order = Order(customer=customer, total=0)
            db.session.add(order)
            db.session.flush()

            # Add 1 to 3 items to the order
            for _ in range(random.randint(1, 3)):
                item = random.choice(items)
                quantity = random.randint(1, 5)
                order_item = OrderItem(order=order, inventory=item, quantity=quantity)
                db.session.add(order_item)
                order.total += item.price * quantity

        db.session.commit()

        # Print some stats
        print(f"Number of users: {User.query.count()}")
        print(f"Number of customers: {Customer.query.count()}")
        print(f"Number of inventory items: {Inventory.query.count()}")
        print(f"Number of orders: {Order.query.count()}")
        print(f"Number of order items: {OrderItem.query.count()}")

if __name__ == "__main__":
    populate_db()
    print("Database populated with example data!")
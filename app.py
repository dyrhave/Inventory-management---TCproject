from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///computeagain.db'
db = SQLAlchemy(app)

order_items = db.Table('order_items',
               db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
               db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True),
               db.Column('quantity', db.Integer, nullable=False)
)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    order = db.relationship('Order', backref='customer', lazy=True)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', secondary=order_items, backref=db.backref('inventory', lazy=True))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    items = db.relationship('Inventory', secondary=order_items ,backref=db.backref('order', lazy=True))


@app.route('/customers', methods=['GET', 'POST'])
def handle_customers():
    if request.method == 'POST':
        data = request.json
        new_customer = Customer(name=data['name'], email=data['email'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"message": "Customer created successfully", "id": new_customer.id}), 201
    else:
        customers = Customer.query.all()
        return jsonify([{
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "order_count": len(c.orders)
        } for c in customers])

@app.route('/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'GET':
        return jsonify({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "orders": [{
                "id": order.id,
                "date": order.date.isoformat(),
                "total": order.total
            } for order in customer.orders]
        })

    elif request.method == 'PUT':
        data = request.json
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        db.session.commit()
        return jsonify({"message": "Customer updated successfully"})

    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully"})


@app.route('/inventory', methods=['GET', 'POST'])
def handle_inventory():
    if request.method == 'POST':
        data = request.json
        new_item = Inventory(name=data['name'], price=data['price'], quantity=data['quantity'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Inventory item created successfully", "id": new_item.id}), 201
    else:
        items = Inventory.query.all()
        return jsonify([{
            "id": i.id,
            "name": i.name,
            "price": i.price,
            "quantity": i.quantity,
            "order_count": i.orders.count()
        } for i in items])

@app.route('/inventory/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_inventory_item(item_id):
    item = Inventory.query.get_or_404(item_id)

    if request.method == 'GET':
        return jsonify({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity,
            "orders": [{
                "id": order.id,
                "date": order.date.isoformat(),
                "customer": order.customer.name
            } for order in item.orders]
        })

    elif request.method == 'PUT':
        data = request.json
        item.name = data.get('name', item.name)
        item.price = data.get('price', item.price)
        item.quantity = data.get('quantity', item.quantity)
        db.session.commit()
        return jsonify({"message": "Inventory item updated successfully"})

    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Inventory item deleted successfully"})


@app.route('/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'POST':
        data = request.json
        customer = Customer.query.get_or_404(data['customer_id'])
        new_order = Order(customer=customer, total=0)

        total = 0
        for item in data['items']:
            inventory = Inventory.query.get_or_404(item['id'])
            if inventory.quantity < item['quantity']:
                return jsonify({"error": f"Not enough {inventory.name} in stock"}), 400
            inventory.quantity -= item['quantity']
            total += inventory.price * item['quantity']
            new_order.items.append(inventory)

        new_order.total = total
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            "message": "Order created successfully",
            "id": new_order.id,
            "total": new_order.total
        }), 201
    else:
        orders = Order.query.all()
        return jsonify([{
            "id": o.id,
            "customer": o.customer.name,
            "date": o.date.isoformat(),
            "total": o.total,
            "items": [{"name": i.name, "quantity": i.quantity} for i in o.items]
        } for o in orders])


@app.route('/orders/<int:order_id>', methods=['GET', 'DELETE'])
def handle_order(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'GET':
        return jsonify({
            "id": order.id,
            "customer": order.customer.name,
            "date": order.date.isoformat(),
            "total": order.total,
            "items": [{"name": i.name, "quantity": i.quantity} for i in order.items]
        })

    elif request.method == 'DELETE':
        for item in order.items:
            item.quantity += order.order_items.filter_by(inventory_id=item.id).first().quantity
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"})
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///computeagain.db')

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship('Order', backref='items')
    inventory = db.relationship('Inventory')

def get_or_404(model, id, abort=None):
    item = model.query.get(id)
    if item is None:
        abort(404, description=f"{model.__name__} with id {id} not found")
    return item

def create_item(model, data):
    new_item = model(**data)
    db.session.add(new_item)
    db.session.commit()
    return new_item

def update_item(item, data):
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()

def delete_item(item):
    db.session.delete(item)
    db.session.commit()


@app.route('/customers', methods=['GET', 'POST'])
@jwt_required()
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
@jwt_required()
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
        update_item(customer, request.json)
        return jsonify({"message": "Customer updated successfully"})
    elif request.method == 'DELETE':
        delete_item(customer)
        return jsonify({"message": "Customer deleted successfully"})


@app.route('/inventory', methods=['GET', 'POST'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Forkert kode eller brugernavn"}), 401


@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    customer_count = Customer.query.count()
    inventory_count = Inventory.query.count()
    order_count = Order.query.count()
    recent_orders = Order.query.order_by(Order.date.desc()).limit(5).all()

    return jsonify({
        "message": f"Welcome {current_user}!",
        "stats": {
            "customer_count": customer_count,
            "inventory_count": inventory_count,
            "order_count": order_count
        },
        "recent_orders": [{
            "id": order.id,
            "customer": order.customer.name,
            "date": order.date.isoformat(),
            "total": order.total
        } for order in recent_orders]
    }), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

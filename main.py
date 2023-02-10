from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import rew_data
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User')

    def to_dict(self):
        return{col.name: getattr(self, col.name) for col in self.__table__.columns}


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return{col.name: getattr(self, col.name) for col in self.__table__.columns}


with app.app_context():
    db.create_all()

    for i in rew_data.users:
        db.session.add(User(**i))
    for i in rew_data.offers:
        db.session.add(Offer(**i))
    for i in rew_data.orders:
        i['start_date'] = datetime.strptime(i['start_date'], '%m/%d/%Y').date()
        i['end_date'] = datetime.strptime(i['end_date'], '%m/%d/%Y').date()
        db.session.add(Order(**i))
    db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def all_users():
    if request.method == 'GET':
        users = User.query.all()
        result = [usr.to_dict() for usr in users]
        return jsonify(result)
    elif request.method == 'POST':
        user_new = json.loads(request.data)
        db.session.add(User(**user_new))
        db.session.commit()
        return ''


@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def one_user(uid):
    user = User.query.get(uid)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_put = json.loads(request.data)
        user.first_name = user_put['first_name']
        user.last_name = user_put['last_name']
        user.age = user_put['age']
        user.email = user_put['email']
        user.role = user_put['role']
        user.phone = user_put['phone']
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return ''


@app.route('/orders', methods=['GET', 'POST'])
def all_orders():
    if request.method == 'GET':
        orders = Order.query.all()
        result = [usr.to_dict() for usr in orders]
        return jsonify(result)
    elif request.method == 'POST':
        order_new = json.loads(request.data)
        db.session.add(Order(**order_new))
        db.session.commit()
        return ''


@app.route('/orders/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def one_order(uid):
    order = Order.query.get(uid)
    if request.method == 'GET':
        return jsonify(order.to_dict())
    elif request.method == 'PUT':
        order_put = json.loads(request.data)
        order.name = order_put['name']
        order.description = order_put['description']
        order.start_date = order_put['start_date']
        order.end_date = order_put['end_date']
        order.address = order_put['address']
        order.price = order_put['price']
        order.customer_id = order_put['customer_id']
        order.executor_id = order_put['executor_id']
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return ''


@app.route('/offers', methods=['GET', 'POST'])
def all_offers():
    if request.method == 'GET':
        offers = Offer.query.all()
        result = [usr.to_dict() for usr in offers]
        return jsonify(result)
    elif request.method == 'POST':
        offer_new = json.loads(request.data)
        db.session.add(Offer(**offer_new))
        db.session.commit()
        return ''


@app.route('/offers/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(uid):
    offer = Offer.query.get(uid)
    if request.method == 'GET':
        return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        offer_put = json.loads(request.data)
        offer.order_id = offer_put['order_id']
        offer.executor_id = offer_put['executor_id']
        db.session.add(offer)
        db.session.commit()
        return jsonify(offer.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return ''


if __name__ == '__main__':
    app.run(debug=True)

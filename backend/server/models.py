from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from app import db
#db=SQLAlchemy()



class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    contacts = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    cart = db.relationship('Cart', backref='user', lazy=True)


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    orders = db.relationship('Order', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    cart = db.relationship('Cart', backref='product', lazy=True)


class Order(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    order_date = db.Column(db.String(120), unique=False, nullable=False)
    delivery_date = db.Column(db.String(120), unique=False, nullable=False)
    delivery_address = db.Column(db.String(120), unique=False, nullable=False)


class Cart(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)


class Review(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    comment = db.Column(db.String(120), unique=False, nullable=False)


class Category(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)


class Admin(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    contacts = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)


class Shop(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    contacts = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    payment_methods = db.Column(db.String(120), unique=False, nullable=False)
    policies = db.Column(db.String(120), unique=False, nullable=False)
    products = db.relationship('Product', backref='shop', lazy=True)
    admins = db.relationship('Admin', backref='shop', lazy=True)

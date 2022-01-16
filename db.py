from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    email =             db.Column(db.String(200), nullable=False, unique=True)
    username =          db.Column(db.String(32), nullable=False)
    password =          db.Column(db.String(32), nullable=False)
    phone_number =      db.Column(db.String(20), nullable=False)
    address =           db.Column(db.String(200), nullable=False)
    age =               db.Column(db.Integer, nullable=False)
    birth_date =        db.Column(db.String(200), nullable=False)
    date_created =      db.Column(db.String(200), default=datetime.now())

    def __repr__(self):
        return f'{self.id} {self.username}'


class ProductCategory(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    name =              db.Column(db.String(200), nullable=False)
    description =       db.Column(db.String(2000), nullable=False)
    
    def __repr__(self):
        return f'{self.id} {self.name}'

class Product(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    name =              db.Column(db.String(200), nullable=False)
    description =       db.Column(db.String(2000), nullable=False)
    category_id =       db.Column(db.Integer, db.ForeignKey(ProductCategory.id), nullable=False)
    price =             db.Column(db.Integer, nullable=False)
    amount =            db.Column(db.Integer, nullable=False)
    discount_rate =     db.Column(db.Integer, nullable=False)    

    productcategory = db.relationship('ProductCategory', backref=db.backref('Product', lazy=False))

    def __repr__(self):
        return f'{self.id} {self.name}'


class CartItem(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    user_id =           db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    product_id =        db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    price =             db.Column(db.Integer, nullable=False)
    amount =            db.Column(db.Integer, nullable=False)
    order_id =          db.Column(db.Integer, nullable=False)
    date_created =      db.Column(db.String(200), default=datetime.now())

    user = db.relationship('User', backref=db.backref('CartItem', lazy=False))
    product = db.relationship('Product', backref=db.backref('CartItem', lazy=False))

    def __repr__(self):
        return f'{self.id}'


class PurchasedOrder(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    user_id =           db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    total_price =       db.Column(db.Integer, nullable=False)
    user_email =        db.Column(db.String(200), nullable=False)
    user_phone =        db.Column(db.String(200), nullable=False)
    user_note =         db.Column(db.String(200), nullable=False)
    address =           db.Column(db.String(200), nullable=False)
    date_created =      db.Column(db.String(200), default=datetime.now())

    user = db.relationship('User', backref=db.backref('PurchasedOrder', lazy=False))

    def __repr__(self):
        return f'{self.id}'

db.create_all()

user1 = User(email='jared@gmail.com', username='jared', password='bruh1234', phone_number='719-327-1876', address='Landline-Colorado-USA', age=19, birth_date=datetime(2002, 7, 31))
user2 = User(email='jacob@gmail.com', username='jacob', password='bruh1234', phone_number='570-609-2534', address='Wyoming-PA-USA', age=48, birth_date=datetime(1973, 8, 4))
user3 = User(email='anthony@gmail.com', username='anthony', password='bruh1234', phone_number='706-321-1318', address='Columbus-Georgia-USA', age=26, birth_date=datetime(1995, 3, 12))

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

print(User.query.all())
from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import sqlalchemy
import hashlib

NON_RESTART_FLAG = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'content'

db = SQLAlchemy(app)

class User(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    email =             db.Column(db.String(200), nullable=False, unique=True)
    username =          db.Column(db.String(32), nullable=False)
    password =          db.Column(db.String(32), nullable=False)
    age =               db.Column(db.Integer, nullable=False)
    date_created =      db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'{self.id} {self.username}'
    
    def validate(self, password):
        return self.password == hashlib.md5(password.encode("utf8")).hexdigest()

    def set_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()


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
    url =               db.Column(db.String(200), nullable=False) 

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
    date_created =      db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
    date_created =      db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User', backref=db.backref('PurchasedOrder', lazy=False))

    def __repr__(self):
        return f'{self.id}'

class Reviews(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    name =              db.Column(db.String(80), nullable=False)
    email =             db.Column(db.String(80), nullable=False)
    text =              db.Column(db.Text)

def init():
    basic_category = ProductCategory(
        name='Кофе',
        description='Это просто кофе.'
    )

    db.session.add(basic_category)

    arabica = Product(
        name='Арабика',
        description='Меньше кофеина.\nБольше липидов и сахаров.\nИнтенсивный и кислотый вкус.\n',
        category_id=1,
        price=2000, 
        amount=100,
        discount_rate=0,
        url='arabica'
    )

    robusta = Product(
        name='Робуста',
        description='Больше кофеина - хорошой энергетик.\nИнтенсивный аромат.\nТерпкий вкус.\n',
        category_id=1,
        price=2000, 
        amount=100,
        discount_rate=0,
        url='robusta'
    )

    liberica = Product(
        name='Либерика',
        description='Большие зерна.\nОчень (!) сильный аромат.\nОчень (!) резкий вкус.\n',
        category_id=1,
        price=2000, 
        amount=100,
        discount_rate=0,
        url='liberica'
    )

    db.session.add(arabica)
    db.session.add(robusta)
    db.session.add(liberica)

    dummy = User(
        email='a@a.ru',
        username='admin',
        password='',
        age=19,
    )
    dummy.set_password('bruh1234')

    db.session.add(dummy)
    db.session.commit()

def create_db():
    db.create_all()

def get_product_by_url(name):
    product = list(Product.query.filter(Product.url == name))
    return product[0] if len(product) == 1 else None

def db_status():
    return os.path.isfile("testdb.db")

def get_products():
    return Product.query.all()

def get_reviews():
    return Reviews.query.all()

def get_cart():
    return CartItem.query.all()

@app.route('/')
def setup():
    return redirect('/index')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        try:
            if User.query.filter(User.username == login).one().validate(password):
                session["login"] = login
                flash(f"Добро пожаловать, {login}!", "success")
                return redirect('/index', code=301)
            flash("Неправильный пароль", "warning")
        except sqlalchemy.exc.NoResultFound:
            flash("Неправильный логин", "danger")
    return render_template('login.html')


@app.route("/logout")
def logout():
    if session.get("login"):
        session.pop("login")
    return redirect("/", code=302)

@app.route('/index')
def render_index():
    return render_template("index.html")

@app.route('/catalogue')
def render_catalogue():
    return render_template("catalogue.html", products=get_products())

@app.route('/<coffee>')
def render_coffee(coffee):
    return render_template("coffee.html", coffee=get_product_by_url(coffee))

if __name__ == '__main__':
    if not db_status():
        create_db()
        init()
    
    app.run(debug=True)
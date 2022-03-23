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

    def inc_amount(self, amount):
        self.amount += amount

    def dec_amount(self, amount):
        self.amount -= amount


class CartItem(db.Model):
    id =                db.Column(db.Integer, primary_key=True)
    user_id =           db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    product_name =      db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    price =             db.Column(db.Integer, nullable=False)
    amount =            db.Column(db.Integer, nullable=False)
    date_created =      db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_visible =        db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref=db.backref('CartItem', lazy=False))
    product = db.relationship('Product', backref=db.backref('CartItem', lazy=False))

    def __repr__(self):
        return f'{self.id}'

    def inc_amount(self, amount):
        self.amount += amount
    
    def update_visibility(self):
        self.is_visible = False


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
        price=3000, 
        amount=100,
        discount_rate=0,
        url='robusta'
    )

    liberica = Product(
        name='Либерика',
        description='Большие зерна.\nОчень (!) сильный аромат.\nОчень (!) резкий вкус.\n',
        category_id=1,
        price=4000, 
        amount=100,
        discount_rate=0,
        url='liberica'
    )

    db.session.add(arabica)
    db.session.add(robusta)
    db.session.add(liberica)

    dummy = None
    if len(list(User.query.all())) == 0:
        dummy = User(
                    email='a@a.ru',
                    username='admin',
                    password='',
                    age=19,
                )
        dummy.set_password('bruh1234')
        db.session.add(dummy)            
    
    dummy_review = Reviews(
        name='Джаред',
        email='a@a.ru',
        text='Отличный кофе. После него я не спал несколько дней.'
    )

    dummy_review1 = Reviews(
        name='Джейкоб',
        email='a@a.ru',
        text='Согласен с Джаредом! Отличный кофе. После него я тоже не спал несколько дней.'
    )

    
    db.session.add(dummy_review)
    db.session.add(dummy_review1)
    db.session.commit()

def create_db():
    db.create_all()

def get_product_by_url(name):
    return Product.query.filter(Product.url == name).one()

def get_product_id_by_url(name):
    return Product.query.filter(Product.url == name).one().id

def db_status():
    return os.path.isfile("testdb.db")

def get_products():
    return Product.query.all()

def get_reviews():  
    return Reviews.query.all()

def get_cart_for_user(user_id):
    return CartItem.query.filter(User.id == user_id)

def disable_cart_for_user(user_id):
    cart = get_cart_for_user(user_id)
    for cart_item in cart:
        cart_item.update_visibility()
        db.session.add(cart_item)
    db.session.commit()

def get_total_price_for_user(user_id):
    cart = get_cart_for_user(user_id)
    total_price = 0
    for cart_item in cart:
        if cart_item.is_visible:
            total_price += cart_item.amount * cart_item.price
    return total_price

@app.route("/404")
def render_404():
    return render_template("404.html")

@app.route('/')
def setup():
    return redirect('/index')

@app.route('/login', methods=["GET", "POST"])
def render_login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        try:
            if User.query.filter(User.username == login).one().validate(password):
                session["login"] = login
                return redirect('/index', code=301)
            flash("Неправильный пароль", "warning")
        except sqlalchemy.exc.NoResultFound:
            flash("Неправильный логин", "warning")
    return render_template('login.html')


@app.route("/logout")
def render_logout():
    if session.get("login"):
        session.pop("login")
        flash("Вы вышли из аккаунта", "success")
    return redirect("/", code=302)

@app.route('/index')
def render_index():
    return render_template("index.html")

@app.route('/reviews', methods=["GET", "POST"])
def render_reviews():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        text = request.form.get("review")
        if name != "" and email != "" and text != "":
            review = Reviews(name=name,
                             email=email,
                             text=text)
            db.session.add(review)
            db.session.commit()
        else:
            flash('Пожалуйста, заполните все поля', 'warning')
    return render_template("reviews.html", reviews=get_reviews())

@app.route('/<login>', methods=['GET', 'POST'])
def render_profile(login):
    if session.get('login') == login:
        user = User.query.filter(User.username == login).one()
        if request.method == 'POST':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')

            if old_password:
                if user.validate(old_password):
                    user.set_password(new_password)
                    flash('Пароль изменен', 'success')
                    db.session.add(user)
                    db.session.commit()
                elif new_password == None:
                    flash('Новый пароль пуст', 'warning')
                else:
                    flash('Старый пароль неверен', 'warning')
        return render_template('profile.html', user=user, cart=get_cart_for_user(user.id), total_price=get_total_price_for_user(user.id))
        
    flash('Пожалуйста, войдите в свой аккаунт, чтобы продолжить', 'warning')
    return redirect('/login', code=301)

@app.route('/buy/<login>', methods=['POST', 'GET'])
def proceed_payment(login):
    if session.get('login') == login:
        user = User.query.filter(User.username == session.get('login')).one()
        
        disable_cart_for_user(user.id)
    
        flash('Спасибо за покупку!', 'success')   

    return redirect('/catalogue')

@app.route('/catalogue')
def render_catalogue():
    return render_template("catalogue.html", products=get_products())

@app.route('/products/<coffee>', methods=['GET', 'POST'])
def render_coffee(coffee):
    if request.method == 'POST':
        if session.get('login') is not None:
            user = User.query.filter(User.username==session.get('login')).one()
            product = get_product_by_url(coffee)
            if user:
                quantity = request.form.get('quantity')
                if get_product_by_url(coffee).amount >= int(quantity):
                    cartitem = None
                    try:
                        cartitem = CartItem.query.filter(sqlalchemy.and_(CartItem.product_name==product.name, CartItem.is_visible==True)).one()
                        cartitem.inc_amount(int(quantity))
                    except sqlalchemy.exc.NoResultFound:
                        cartitem = CartItem(
                            user_id=user.id,
                            product_name=product.name,
                            price=product.price,
                            amount=quantity
                        )

                    product.dec_amount(int(quantity))
                    db.session.add(cartitem)
                    db.session.commit()

                    flash('Товар добавлен в корзину', 'success')
                else:
                    flash('Недостаточно товара на складe', 'warning')
                    
            return render_template("coffee.html", coffee=get_product_by_url(coffee))

        flash('Пожалуйста, войдите в свой аккаунт, чтобы продолжить', 'warning')
    return render_template("coffee.html", coffee=get_product_by_url(coffee))

if __name__ == '__main__':
    if not db_status():
        create_db()
        init()
    
    app.run(host='0.0.0.0')
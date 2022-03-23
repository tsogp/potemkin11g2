import sqlalchemy, flask
from app.models import *
from app.setup import *

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

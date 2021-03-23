import os
import random
from flask import Flask, render_template, redirect, session, flash, url_for, jsonify, request
from models import *
from forms import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc
import json
import os
import stripe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///shop_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
# app.config["SECRET_KEY"] = "usafa1993"
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'usafa1993')
app.config["UPLOADED_IMAGES_DEST"] = "uploads/images"

connect_db(app)

# Set image storage information
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
patch_request_class(app, 1024 * 1024)

# Stripe secret key
stripe.api_key = "sk_test_HjmEiebcMzZHRfIBgPfeWPeO00Af8WCWzO"


@app.route('/')
def index():
    """Main route for initial user store view"""
    products = Product.query.all()
    return render_template('store.html', products=products)


@app.route('/product/<id>')
def product(id):
    """View individual product when user click on the product image or title. Page shows the selected product's details"""
    product = Product.query.filter_by(id=id).first()
    form = AddToCart()

    return render_template('view-product.html', product=product, form=form)


@app.route('/quick-add/<id>')
def quick_add(id):
    """Route whe user clicks on the 'quickadd' shopping cart at the bottom left of product. Adds a single item to the cart."""
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'id': id, 'quantity': 1})
    session.modified = True
    flash(f'Added 1 item to cart', "success")

    return redirect(url_for('index'))


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """Route when user adds product to cart."""

    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()

    if form.validate_on_submit():

        session['cart'].append({
            'id': form.id.data,
            'quantity': form.quantity.data
        })
        session.modified = True

    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    """Cart route. Calls the handle_cart method to collect all the information from the items in the cart"""
    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()

    return render_template('cart.html', products=products, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total)


@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    """Route used to delete an item from the current cart session."""
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/admin')
def admin():
    """Main route for the admin panel. User must first be logged in to view the dashboard"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    products = Product.query.order_by(Product.id.desc()).all()
    products_in_stock = Product.query.filter(Product.stock > 0).count()

    orders = Order.query.all()

    return render_template('/admin/admin.html', title='Admin', products=products, products_in_stock=products_in_stock, orders=orders)


@app.route('/admin/order/<order_id>')
def order(order_id):
    """Route for viewing the order details tab on the main admin dashboard"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    order = Order.query.filter_by(id=int(order_id)).first()

    return render_template('/admin/view-order.html', title='Order Overview', order=order)


@app.route("/admin/order/<int:id>", methods=['DELETE'])
def delete_order(id):
    """Route for deleting an order from the orders tab on the admin dashboard"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify(msg="Deleted")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Route for users to create an account"""
    form = SignupForm()
    if "user_id" in session:
        return redirect('/admin')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        new_user = User.register(username, password, email)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('signup.html', form=form)
        session['user_id'] = new_user.id
        session['user_username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/admin')

    return render_template('admin/signup.html', form=form)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Main route for checkout. Calls handle_cart to get and calculate all cart information."""
    form = Checkout()
    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart(
    )

    if form.validate_on_submit():
        order = Order()
        form.populate_obj(order)
        # Generate random order reference by randomizing the letters in 'ABCDE'
        order.reference = ''.join([random.choice('ABCDE') for _ in range(5)])
        order.status = 'PENDING'

        for product in products:
            order_item = Order_Item(quantity=product['quantity'],
                                    product_id=product['id'])
            order.items.append(order_item)
            product = Product.query.filter_by(id=product['id']).update(
                {'stock': Product.stock - product['quantity']})

        db.session.add(order)
        db.session.commit()

        session['cart'] = []
        session.modified = True
        return redirect(url_for('index'))

    return render_template('checkout.html',
                           form=form,
                           grand_total=grand_total,
                           grand_total_plus_shipping=grand_total_plus_shipping,
                           quantity_total=quantity_total)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Route for user login"""
    form = LoginForm()
    if "user_id" in session:
        return redirect('/admin')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            session['user_username'] = user.username

            return redirect('/admin')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('admin/login.html', title='Login', form=form)


@app.route('/logout')
def logout_user():
    """Route for user logout"""
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/product', methods=['GET', 'POST'])
def add():
    """Route for adding products to the inventory"""
    form = AddProduct()
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    if form.validate_on_submit():
        try:
            name = form.name.data
            price = form.price.data
            stock = form.stock.data
            description = form.description.data
            image = form.image.data

            if image == None:
                img_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/6/65/Happy_fun_ball.jpg/300px-Happy_fun_ball.jpg'
            else:
                # Show URL
                img_url = images.url(images.save(image))

            new_product = Product(
                name=name, price=price, stock=stock, description=description, image=img_url)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('admin'))
        except UploadNotAllowed:
            return '<h1>File type not allowed</h1>'
    return render_template('/admin/add-product.html', title='Add/Edit Product', form=form)


# Get JSON data for all product
@app.route("/api/product")
def list_product():
    """Returns json for all product in database."""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    all_product = [product.to_dict() for product in Product.query.all()]
    return jsonify(product=all_product)


@app.route("/api/product/<int:id>")
def get_product(id):
    """Returns json for selected product"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    product = Product.query.get_or_404(id)
    return render_template("/admin/edit.html", product=product)


@app.route("/api/product/<int:id>", methods=['PATCH'])
def update_product(id):
    """Updates product information"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    form = UpdateProduct()
    data = request.json

    product = Product.query.get_or_404(id)

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.description = data.get('description', product.description)
    # product.image = data.get('image', product.image)

    db.session.add(product)
    db.session.commit()

    return jsonify(product=product.to_dict())


@app.route("/api/product/<int:id>", methods=['DELETE'])
def delete_product(id):
    """Deletes selected product"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(msg="Deleted")


def handle_cart():
    """Calculate all cart information"""
    products = []
    grand_total = 0
    index = 0
    quantity_total = 0

    for item in session['cart']:
        product = Product.query.filter_by(id=item['id']).first()

        quantity = int(item['quantity'])
        price = product.price / 100
        total = quantity * price
        grand_total += total
        index += 1

        quantity_total += quantity

        products.append({
            'id': product.id,
            'name': product.name,
            'price': price,
            'image': product.image,
            'quantity': quantity,
            'total': total,
            'index': index
        })

    grand_total_plus_shipping = grand_total + 10

    return products, grand_total, grand_total_plus_shipping, quantity_total


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    """Receives cart total pricing and sends that to Stripe for payment processing"""
    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()
    # print(grand_total_plus_shipping)
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total_plus_shipping * 100),
            currency='usd'
        )
        # print(intent)
        print(f"the grand total plus shipping is: {grand_total_plus_shipping}")
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 403

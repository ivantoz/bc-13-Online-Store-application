import os
import hashlib
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask import Flask, render_template, session, redirect, url_for, flash, request,send_from_directory
from flask.ext.script import Shell
from forms import LoginForm, ProductsForm,RegistrationForm
import models
from models import db
from models import Products
import flask_login
from models import User


app= Flask(__name__)
app.config['SECRET_KEY'] = '7z(!RlYYx4vV$ZZE'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)
app.secret_key = '6XeA3e@&HTM1t7IF78'


@login_manager.user_loader
def load_user(user_id):
    """Used by Flask-Login to get a user by its id."""
    try:
        ret = User.query.get(user_id)
        ret.authenticated = True
    except Exception as ex:
        print (type(ex))
        print (ex)
        ret = None
    return ret


def check_login(username, password):
    """Checks whether or not the given username and password are valid."""
    user = User.query.filter(User.email == username).first()
    if user:
        hasher = hashlib.sha1()
        salt, pwd = user.password.split('$', 2)
        hasher.update(salt + password)
        if hasher.hexdigest() == pwd:
            user.authenticated = True
            return user
        else:
            return False
    else:
        return False



@app.route('/favicon.ico')
def favicon():
    """Reroute requests to the favicon to the correct location in static."""
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def landing():
	return render_template("landing_page.html")




@app.route('/index')
def index():
    products = Products.query.all()
    return render_template("index.html", products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if not flask_login.current_user.is_authenticated:
		to_page = request.args.get("next")
		if to_page == url_for("logout"):
			to_page = False
		form = LoginForm()
		if form.is_submitted():
			if form.validate():
				user = check_login(form.email.data, form.password.data)
				if user:
					flask_login.login_user(user, form.remember_me.data)
					flash("Logged in successfully.", "success")
					return redirect(to_page or url_for("view"))
				else:
					flash("Invalid Username/Password", "error")
			else:
				for key, msg in form.errors.items():
					flash("Could not validate " + key + ": " + ", ".join(msg),
						  "error")
		return render_template("login.html", form=form)
	else:
		flash("You are already logged in!", "info")
		return redirect(request.args.get("next") or url_for("view"))




@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(request.args.get("next") or url_for("login"))

@flask_login.login_required
@app.route('/admin/displayproducts', methods=['GET', 'POST'])
def view():
    if flask_login.current_user.is_authenticated:
		products = Products.query.all()
		return render_template('displayproducts.html', products=products, table=products)
    else:
        return redirect(request.args.get("next") or url_for("login"))

@flask_login.login_required
@app.route('/admin/addproduct', methods=['GET', 'POST'])
def products():
    if flask_login.current_user.is_authenticated:
        form = ProductsForm(request.form)
        if request.method == 'GET':
            return render_template('products.html', title='Add Products', form=form)
        if request.method == 'POST':
            title = Products.query.filter_by(title=form.title.data).first()
            products = Products(title=form.title.data,
                                description=form.description.data,
                                price=form.price.data)
            db.session.add(products)
            db.session.commit()
            # return redirect(url_for('products'))
            return render_template('displayproducts.html', products=products, table=products)

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.name.data).first()
            if user is None:
                user = User(username=form.name.data)
                db.session.add(user)
                session['known'] = False
            else:
                session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('index'))
        return render_template('index.html',
                               form=form, name=session.get('name'),
                               known=session.get('knoswn', False))

        return render_template('index.html', form=form, name=session.get('name'))
    else:
        return redirect(request.args.get("next") or url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if not flask_login.current_user.is_authenticated:
        to_page = request.args.get("next")
        if to_page == url_for("logout"):
            to_page = False
        form = RegistrationForm()
        if form.is_submitted():
            if form.validate():
                try:
                    db.session.add(User(form.email.data, form.username.data,
                        form.password.data, form.name.data, form.phone.data))
                    db.session.commit()
                    flash("Congratualtions, " + (form.name.data or
                        form.username.data) + "! You have registered\
                                successfully!", "success")
                    return redirect(to_page or url_for("view"))
                except:
                    if not app.debug:
                        flash("We're sorry, we were unable to register you.\
                                Feel free to try again.", "error")
                    else:
                        raise
            else:
                for key, msg in form.errors.items():
                    flash("Could not validate " + key + ": " + ", ".join(msg),
                            "error")
        return render_template("register.html", form=form)
    else:
        flash("You are already logged in!", "info")
        return redirect(request.args.get("next") or url_for("view"))


if __name__ == '__main__':
	app.run(debug=True)

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired(), Length(6, 64), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class ProductsForm(Form):
	title = StringField('Title', validators=[DataRequired(), Length(1, 64)])
	description = StringField('Description', validators=[DataRequired(), Length(1, 300)])
	price = IntegerField('Price', validators=[DataRequired()])
	save = SubmitField('Save')


class RegistrationForm(LoginForm):
	username = StringField('Username', validators=[DataRequired(),Length(2, 64)])
	email = StringField('Email Address', validators = [DataRequired(),Length(6, 64),Email(u'Invalid Email Address')])
	name = StringField('Full Names', validators=[DataRequired(),Length(6, 64)])
	phone = StringField('Phone Number', validators=[DataRequired(), Length(10, 20)])
	password = PasswordField('New Password', validators=[DataRequired(),Length(6,20),EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	admin = BooleanField('Make me an Admin')
	submit = SubmitField('Register')





#class HomeForm(Form):


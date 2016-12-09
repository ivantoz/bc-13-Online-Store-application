import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime
#import datetime
from utilities import str_to_digits, generate_encrypted_password

app = Flask(__name__)

# Alias a function
#now = datetime.date.strftime("%Y-%m-%d %H:%M:%S")
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(300))
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<products {} {} {}>'.format(self.title, self.description, self.price)


class User(db.Model):
    __tablename__ = 'User'

    __table_args__ = {}

    # column definitions
    date_created = db.Column(u'date_created', db.DateTime(), nullable=False)
    date_modified = db.Column(u'date_modified', db.DateTime(), nullable=False)
    email = db.Column(u'email', db.String(length=128), nullable=False,
                      unique=True)
    id = db.Column(u'id', db.Integer(), primary_key=True, nullable=False)
    name = db.Column(u'name', db.String(length=64))
    password = db.Column(u'password', db.String(length=64), nullable=False)
    phone = db.Column(u'phone', db.BigInteger())
    username = db.Column(u'username', db.String(length=32), nullable=False,
                         unique=True)
    authenticated = False

    def __init__(self, email, username, password, name=None, phone=None):
        self.name = name if name != '' else None
        self.username = username
        self.email = email
        self.password = generate_encrypted_password(password)
        self.phone = str_to_digits(phone)
        current_time = datetime.utcnow()
        self.date_created = current_time
        self.date_modified = current_time
        self.authenticated = False

    def __repr__(self):
        return "<User id: {id}, username: {usn}, name: {name},>".format(
            id=self.id, name=self.name, usn=self.username,
            auth=self.authenticated)

        # Methods for Flask-Login

    def get_id(self):
        return unicode(self.id)

    def is_anonymous(self):
        return not isinstance(self.id, long)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.is_authenticated()

    def is_admin(self):
        # TODO: Test whehter admin relationship exists
        return False


class Admin(db.Model):
    __tablename__ = 'Admin'

    __table_args__ = {}

    # column definitions
    date_created = db.Column(u'date_created', db.DateTime(), nullable=False)
    date_modified = db.Column(u'date_modified', db.DateTime(), nullable=False)
    id = db.Column(u'id', db.Integer(), primary_key=True, nullable=False)
    level = db.Column(u'level', db.String(length=8), nullable=False)
    user_id = db.Column(u'user_id', db.Integer(), db.ForeignKey('User.id'))

    def __init__(self, level, user_id):
        self.level = level
        self.user_id = user_id
        current_time = datetime.utcnow()
        self.date_created = current_time
        self.date_modified = current_time

    # db.relationship definitions
    User = db.relationship('User', primaryjoin='Admin.user_id==User.id',
                           backref=db.backref('User', lazy='joined'))


if __name__ == '__main__':
    manager.run()
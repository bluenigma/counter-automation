from app import db, login
from datetime import datetime
from flask import current_app, url_for
from flask_login import UserMixin
import json
import redis
import rq
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

class Counter(db.Model):
    __tablename__ = 'counters'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    sn = db.Column(db.String(32), db.ForeignKey('units.sn'))
    black_total = db.Column(db.Integer)
    color_total = db.Column(db.Integer)

    def __repr__(self):
        return(
        f'<{self.date}> Counter report No. {self.id}'
        f'<Black: {self.black_total}>'
        f'<Color: {self.color_total}>')

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    sn = db.Column(db.String(32), unique=True)
    vendor = db.Column(db.String(64))
    model = db.Column(db.String(32))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    counters = db.relationship('Counter', backref='units')
    client = db.relationship('Client', backref='units')

    def __repr__(self):
        return(f'<Unit: {self.sn}, Model: {self.model}>')

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64))
    black_rate = db.Column(db.Float)
    color_rate = db.Column(db.Float)
    min_monthly_pay = db.Column(db.Integer)
    units = db.relationship('Unit', backref='clients')
    # --------- Contact info ---------
    address = db.Column(db.String(128))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    notes = db.Column(db.String(256))
    # --------------------------------

    def __repr__(self):
        return(f'<Client: [{self.name}]>')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.Column(db.String(32))    # with flask-praetorian
    # --------- Contact info -----------
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    notes = db.Column(db.String(256))
    # ----------------------------------

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_email(self, email):
        self.email = email

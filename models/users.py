from extensions import db
from datetime import datetime

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	created_on = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
	confirmed = db.Column(db.SmallInteger, default=0)
	confirmed_on = db.Column(db.DateTime, nullable=True)

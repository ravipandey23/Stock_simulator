from datetime import datetime
from security import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import column_property, relationship, backref

from sqlalchemy import Table, Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@login_manager.user_loader
def load_user(username):
    return User.query.get(str(username))


class User(UserMixin,db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name =  db.Column(db.String(20), nullable=False)
	# username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	since = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


	username = db.Column(db.String(20), ForeignKey('portfolio_main.username'))
	portfolio_main = db.relationship("Portfolio_main", back_populates="user")



	def __repr__(self):
		return f"User('{self.name}', '{self.username}', '{self.email}', '{self.image_file}', '{self.since}')"



class Portfolio_main(db.Model, UserMixin):
	__tablename__ = 'portfolio_main'
	# id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), primary_key=True)
	acc_value = db.Column(db.Float(2), nullable=False,default= 200000.00)
	buy_pow = db.Column(db.Float(2),nullable=False, default= 200000.00)
	annual_ret = db.column_property(acc_value/2000)

	#one to one relationship between User and portfolio_main
	user = db.relationship("User", uselist=False, back_populates="portfolio_main")

	# one to many relationship from portfolio_main to Portfolio_second
	portfolios = db.relationship("Portfolio_second", backref="portfolio_main")

	# user_id = Column(Integer, ForeignKey('user.id'))
	# user = relationship("User", back_populates="portfolio_main")

	def __repr__(self):
		return f"User('{self.username}', '{self.acc_value}', '{self.buy_pow}', '{self.annual_ret}')"
	def get_id(self):
		return (self.username)

class Portfolio_second(db.Model, UserMixin):
	__tablename__ = 'Portfolio_second'
	id = db.Column(db.Integer, primary_key=True)
	# username = db.Column(db.String(20), nullable=False)
	username = db.Column(db.String(20), ForeignKey('portfolio_main.username'))
	sec_symbol = db.Column(db.String(10), nullable=False)
	sec_name = db.Column(db.String(100), nullable=True)
	sec_type = db.Column(db.String(50), nullable=True)
	quantity = db.Column(db.Integer, nullable=False)
	pur_price = db.Column(db.Float(2), nullable=False)
	curr_price = db.Column(db.Float(2),nullable=True)
	total_value = db.column_property(quantity*curr_price)
	today_change = db.Column(db.Float(2), nullable=True)
	percent_change = db.Column(db.Float(2), nullable=True)
	date =  db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

	# username = db.Column(db.String(20), ForeignKey('portfolio_main.username'))



	def __repr__(self):
		return f"User('{self.username}', '{self.sec_symbol}', '{self.quantity}' '{self.total_value}')"

	def get_id(self):
		return (self.username)





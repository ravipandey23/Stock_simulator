from flask_wtf import FlaskForm
import string
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from security.models import User
import re

class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate(self):
        password = self.password.data
        confirm_password = self.confirm_password.data;
        if(password != confirm_password):
            flash('Confirm password should be same as password.', 'danger')
            return False

        name = self.name.data;
        if(len(name)<2 or len(name)>20):
            flash('Length of name should be between 2 to 20 characters.', 'danger')
            return False
        contains_specialchars = self.check_specialchars(password)
        contains_nums = self.check_nums(password)
        contains_alphabets = self.check_alphabets(password)

        check_username = self.check_username(self.username.data)
        check_email = self.check_email(self.email.data)
        if not (contains_alphabets and contains_nums and contains_specialchars):
            flash('Password must contain atleast one special character, one number and atleast one alphabet.', 'danger')
            return False
        else:
            if not (check_username and check_email):
                return False
        return True

    def check_username(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            flash('That username is taken. Please choose a different one.', 'danger')
            return False
        else:
            if(len(username)<5 or len(username)>20):
                flash('Length of username should be between 5 to 20 characters.', 'danger')
                return False
        return True

    def check_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user:
            flash('That email is taken. Please choose a different one.', 'danger')
            return False
        else:
            chk = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
            if chk==None:
                flash('Invalid Email format.', 'danger')
                return False
        return True

    def check_specialchars(self, password):
        special_chars = list(set(string.punctuation))
        for character in password:
            if character in special_chars:
                return True
        return False

    def check_nums(self, password):
        for character in password:
            if character.isdigit():
                return True
        return False

    def check_alphabets(self, password):
        alphabets = string.ascii_lowercase + string.ascii_uppercase
        for character in password:
            if character in alphabets:
                return True
        return False


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')   



class Getstockprice(FlaskForm):
    symbol = StringField('symbol',validators=[DataRequired()])
    

class Buy_stock(FlaskForm):
    symbol = StringField('symbol',validators=[DataRequired()])
    quantity = IntegerField('quantity',validators=[DataRequired()])

class Sell_stock(FlaskForm):
    symbol = StringField('symbol',validators=[DataRequired()])
    quantity = IntegerField('quantity',validators=[DataRequired()])


class get_symbol(FlaskForm):
    symbol = StringField('symbol',validators=[DataRequired()])
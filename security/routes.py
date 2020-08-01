import os
import secrets
from flask import render_template, url_for, flash, redirect, request, session
from security import app, db, bcrypt
from security.forms import RegistrationForm, LoginForm, Getstockprice, Buy_stock, Sell_stock,get_symbol
from security.models import User, Portfolio_main, Portfolio_second
from flask_login import login_user, current_user, logout_user, login_required
from security import api_prog, orm
import datetime



@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return render_template('sidebar.html', username1=current_user.username,  acc_value="%.2f" % float(orm.find_acc_val(current_user.username)), buy_value = "%.2f" % current_user.portfolio_main.buy_pow)
    else:
        return render_template('index.html')
    

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        port_main = Portfolio_main(username=form.username.data)
        db.session.add(port_main)
        db.session.commit()
        # port_second = Portfolio_second(username=form.username.data)
        # db.session.add(port_second)
        # db.session.commit()
        flash(f'Account created for {form.username.data}, Now you can login to access your account!', "success")
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('sidebar'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash('You have been logged in!', 'success')
            # return redirect(next_page) if next_page else redirect(url_for('about'))
            return redirect(next_page) if next_page else redirect(url_for('sidebar'))
            # return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')           
    return render_template('login.html', form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/sidebar")
@login_required
def sidebar():
    return render_template('sidebar.html', username1=current_user.username,  acc_value="%.2f" % float(orm.find_acc_val(current_user.username)), buy_value = "%.2f" % current_user.portfolio_main.buy_pow)


@app.route("/trade")
@login_required
def trade():
    return render_template('trade.html',   acc_value="%.2f" % float(orm.find_acc_val(current_user.username)), buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret))

@app.route("/about")
def about():
	return "<h1 style='color:pink'>About Page</h1>"

 
@app.route("/research")
@login_required
def research():
    return render_template('research.html', title='Account')


@app.route('/getstockprice', methods = ["GET","POST"])
@login_required
def getstockprice():
    form = Getstockprice()
    #symbol = request.form['symbol']
    symbol = form.symbol.data
    if symbol == "":
        flash(f'Please give required input!', "danger")
        return render_template('research.html')
    payload_from_wrapper = api_prog.get_stock_details(symbol)
    name, price, change, per_change, high, low = payload_from_wrapper
    if name == "":
        flash(f'Invalid company symbol!', "danger")
        return render_template('research.html')
    return render_template('getstockprice.html',name=name,price=price, change= "%.2f" %change, change_per="%.2f" %per_change, high="%.2f" %high, low="%.2f" %low)


@app.route("/portfolio")
@login_required
def portfolio():
    port_second_data = orm.get_tuples(current_user.username)
    # npv=[]
    temp=0.0
    date = 0
    if port_second_data is not False:
        # [ (ticker, price, quantity ) ]
        for stocks in port_second_data:
            price, today_ch, per_ch = api_prog.get_stock_change(stocks[2])
            if price == 0:
                flash(f'API Error 403!', "danger")
                return render_template('portfolio.html',stocks=[])
            stocks[7] = price 
            stocks[8] = float(stocks[5]) * float(price)
            stocks[8] = "%.2f" % stocks[8]
            temp=float(stocks[5]) * (float(price)-float(stocks[6]))
            # npv.append(temp)
            stocks[2] = stocks[2].upper()
            # today_ch, per_ch = api_prog.get_stock_change(stocks[2])
            stocks[9] = "%.2f" % today_ch
            stocks[10] = "%.2f" % per_ch
            # stocks[10] = today_ch
            date = datetime.date.today()
            # stocks[12] = temp
        return render_template('portfolio.html',  stocks=port_second_data, acc_value="%.2f" % float(orm.find_acc_val(current_user.username)), buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret) , date=date)
    else:
        return render_template('portfolio.html',NPV='0', stocks=[])

    # return render_template('portfolio.html')


@app.route("/buy_stock", methods = ["GET","POST"])
@login_required
def buy_stock():
    form = Buy_stock()
    symbol = request.form['symbol']
    quantity = request.form['quantity']
    # symbol=form.symbol.data
    # quantity=form.quantity.data
    if quantity == "" or symbol == "":
        flash(f'Please give required input!', "danger")
        return render_template('trade.html', buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret))    
    name, price = api_prog.get_stock_price(symbol)
    net = float(quantity)*float(price)
    if price == 0:
        flash(f'API Error 403!', "danger")
        return render_template('trade.html', buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret))
    if net > current_user.portfolio_main.buy_pow:
        flash(f'Insufficient Account Balance!', "danger")
        return render_template('trade.html', buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret))
    else:
        orm.update_port_main(current_user.username, net)
        b_p = current_user.portfolio_main.buy_pow
        orm.update_port_sec(current_user.username,symbol,name,quantity,price)
        flash(f'Purchased Successfully!', "success")
    return render_template('buy_stock.html', buy_pow= "%.2f" % b_p, sec_name= name, quant=quantity, sec_price=price)
 
    

@app.route("/sell", methods = ["GET","POST"])
@login_required
def sell():
    form = Sell_stock()
    symbol = request.form['symbol']
    quantity = request.form['quantity']
    if quantity == "" or symbol == "":
        flash(f'Please give required input!', "danger")
        return render_template('trade.html', buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret))        
    name, price = api_prog.get_stock_price(symbol)
    net = float(quantity)*float(price)
    if price == 0:
        flash(f'API Error 403!', "danger")
        return render_template('trade.html', buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret))
    if orm.validate_quantity(current_user.username, symbol,quantity) is False:
        flash(f'Not Enough quantity to sold!', "danger")
        return render_template('trade.html', buy_power= "%.2f" % float(current_user.portfolio_main.buy_pow), ann_return= "%.2f" % float(current_user.portfolio_main.annual_ret))
    else:
        orm.update_port_sec_on_sell(current_user.username, symbol,quantity, price)
        b_p = current_user.portfolio_main.buy_pow
        flash(f'Sold Successfully!', "success")
    return render_template('sell.html',  buy_pow= "%.2f" % b_p, sec_name= name, quant=quantity, sec_price=price)


@app.route("/getsymbol", methods = ["GET","POST"])
@login_required
def getsymbol():
    form = get_symbol()
    name = request.form['symbol']
    # name = form.symbol.data
    if name == "":
        flash(f'Please give required input!', "danger")
        return render_template('research.html')
    symbol = api_prog.get_company_sym(name)
    if symbol is False:
        flash(f'company name invalid!', "danger")
        return render_template('research.html')
    return render_template('getsymbol.html',name=name,symbol=symbol)

@app.route("/contact")
@login_required
def contact():
    return render_template('contact.html', title='Account')
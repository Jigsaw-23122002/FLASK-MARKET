from flask import redirect, render_template,flash,request
from markets import app
from markets import models
from markets import forms
from markets.forms import LoginForm, PurchaseForm, RegisterForm, SellForm
from markets.models import Item,User
from markets import db
from flask_login import current_user, login_user,logout_user,login_required

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required
def market():
    purchase_form=PurchaseForm()
    sell_form=SellForm()
    if request.method=='POST':
        purchased_item=request.form.get('purchased_item')
        if purchased_item:
            purchased_item=purchased_item.strip()
            p_item_object=Item.query.filter_by(barcode=purchased_item).first()
            if p_item_object:
                if current_user.budget-p_item_object.price>=0:
                    p_item_object.owner=current_user.id
                    current_user.budget-=p_item_object.price
                    db.session.commit()
                    flash(f"You have successfully purchased the item {p_item_object.name} for {p_item_object.price}$!",category="success")
                else:
                    flash("Not Enough balance to purchase this item.",category="danger")

        sold_item=request.form.get('sold_item')
        print(sold_item)
        s_item_object=Item.query.filter_by(barcode=sold_item).first()
        if s_item_object:
            s_item_object.owner=None
            current_user.budget+=s_item_object.price
            db.session.commit()
            flash(f"You have successfully sold {s_item_object.name} for {s_item_object.price}$",category="success")

        return redirect('/market')

    if request.method=='GET':
        items=Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items,purchase_form=purchase_form,sell_form=sell_form,owned_items=owned_items)

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        createUser=User(username=form.username.data,email=form.email.data,password_hash=form.password1.data)
        db.session.add(createUser)
        db.session.commit()
        login_user(createUser)
        flash(f'Account created successfully! You are now logged in as {createUser.username}',category="success")
        return redirect('/market')

    if form.errors!={}:
        for err in form.errors.values():
            flash(f'there was an error in creating a user:{err}',category="danger")

    return render_template('register.html',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.password_hash==form.password.data:
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}',category="success")
            return redirect('/market')

        else:
            flash("Invalid Credentials",category="danger")
    
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("User logged out successfully")
    return redirect('/')
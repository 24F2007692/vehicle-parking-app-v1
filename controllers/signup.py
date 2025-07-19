from flask import render_template,redirect,request,url_for,flash,session
from app import app
from models.models import User,db

@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('mail')
    password = request.form.get('pass')
    name = request.form.get('name')
    address = request.form.get('address')
    pincode = request.form.get('pincode')

    if email != "" and password != "" and name != "" and address != "" and pincode != "":
        user = User(email=email, password=password, name=name,address=address, pincode=pincode)

        if User.query.filter_by(email=email).first():
            flash('user with this email already exists')
            return redirect(url_for('signup'))
    
    else:
        flash('Enter all details')
        return redirect(url_for('signup'))

    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    session['user_name'] = user.name
    flash("User sucessfully registered")
    return redirect(url_for('dashboard'))
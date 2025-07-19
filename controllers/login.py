from flask import render_template,redirect,request,url_for,flash,session
from app import app
from models.models import User

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('mail')
    password = request.form.get('pass')

    if email != "" and password != "":
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User does not exist")
            return redirect(url_for('login'))
        
        if not user.chk_pass(password):
            flash('Incorrect password')
            return redirect(url_for('login'))
        session['user_id'] = user.id
        session['user_name'] = user.name
    else:
        flash('mat kar lala mat kar!!')
        return redirect(url_for('login'))
    flash(f"welcome {user.role}")
    return redirect(url_for('dashboard'))
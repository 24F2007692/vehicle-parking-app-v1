from flask import render_template, redirect, url_for, flash, session
from app import app
from models.models import User

@app.route('/allusers')
def allusers():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))
    users = User.query.all()
    data = [[user.id, user.email, user.name, user.address, user.pincode]
            for user in users]
    return render_template("admin_all_users.html", data=data)
from flask import request, redirect, url_for, flash, session
from app import app

@app.route("/search_lot", methods=['POST'])
def search_lot():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    location = request.form.get('location')

    if location:
        return redirect(url_for('dashboard', location=location))
    else:
        flash("Please enter a valid location")
        
    return redirect(url_for('dashboard'))
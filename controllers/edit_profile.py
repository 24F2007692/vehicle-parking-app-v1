from flask import render_template, request, redirect, url_for, flash, session
from models.models import User, db
from app import app


@app.route("/editprofile", methods=["GET", "POST"])
def editprofile():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == "POST":
        old_pass = request.form.get('O_pass')
        new_pass = request.form.get('N_pass')

        if not old_pass:
            flash('Please enter your old password to update your profile')
            return redirect(url_for('editprofile'))

        if not user.chk_pass(old_pass):
            flash('Old password is incorrect')
            return redirect(url_for('editprofile'))

        new_name = request.form.get('name')
        new_address = request.form.get('address')
        new_pincode = request.form.get('pincode')

        if not new_name or not new_address or not new_pincode:
            flash('do not leave any field empty')
            return redirect(url_for('editprofile'))


        is_changed = False

        if new_name != user.name:
            user.name = new_name
            is_changed = True

        if new_address != user.address:
            user.address = new_address
            is_changed = True

        if new_pincode != user.pincode:
            user.pincode = new_pincode
            is_changed = True

        if new_pass:
            user.password = new_pass
            is_changed = True

        if is_changed:
            db.session.commit()
            flash('Profile updated successfully')
        else:
            flash('No changes detected')

        session['user_name'] = user.name
        return redirect(url_for('dashboard'))

    return render_template("edit_profile.html", user=user)

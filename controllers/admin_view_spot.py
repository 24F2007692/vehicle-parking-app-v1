from flask import render_template, redirect, url_for, flash, session
from app import app
from models.models import ParkingSpot

@app.route("/view_spot/<int:spot_id>", methods=["GET", "POST"])
def view_spot(spot_id):

    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    if not spot:
        flash("Spot not found")
        return redirect(url_for('dashboard'))

    return render_template("admin_view_spot.html", status=spot.status, spot_no=spot.spot_no, spot_id=spot.id)
from flask import render_template, redirect, url_for, flash, session
from app import app
from models.models import ParkingLot,Reservation,ParkingSpot
from datetime import datetime, timezone,timedelta

IST = timezone(timedelta(hours=5, minutes=30))

@app.route("/O_spot/<int:spot_id>")
def O_spot(spot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    O_spot = Reservation.query.filter_by(spot_id=spot_id).first()
    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    lot = ParkingLot.query.filter_by(id=spot.lot_id).first()

    if O_spot:
        booking_time = O_spot.booking_time
        if booking_time.tzinfo is None:
            booking_time = booking_time.replace(tzinfo=IST)
            curr_time = datetime.now(IST)
            duration = (curr_time - booking_time).total_seconds() / 3600
            duration = max(duration, 0.01)
            price_per_hr = float(lot.price_per_hr)
            total_cost = round(duration * price_per_hr, 2)
        return render_template("admin_O_spot.html", O_spot=O_spot, total_cost=total_cost,price_per_hr=round(price_per_hr),lot=lot)

    return redirect(url_for('dashboard'))
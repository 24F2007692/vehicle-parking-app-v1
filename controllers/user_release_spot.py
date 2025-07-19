from flask import request,render_template, redirect, url_for, flash, session
from models.models import  ParkingLot, ParkingSpot, Reservation, db
from datetime import datetime, timezone, timedelta
from app import app


IST = timezone(timedelta(hours=5, minutes=30))



@app.route("/release/<int:res_id>", methods=['GET', 'POST'])
def release(res_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    res = Reservation.query.get(res_id)
    if not res:
        flash("Reservation not found")
        return redirect(url_for('dashboard'))

    spot = ParkingSpot.query.get(res.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)

    if request.method == 'POST':
        res.Leaving_timestamp = datetime.now(IST)
        spot.status = 'A'
        res.parking_cost = request.form.get("total_cost")
        res.spot_id = None
        db.session.commit()
        flash("Spot released successfully")
        return redirect(url_for('dashboard'))

    booking_time = res.booking_time
    if booking_time.tzinfo is None:
        booking_time = booking_time.replace(tzinfo=IST)
    release_time = datetime.now(IST)


    duration = (release_time - booking_time).total_seconds() / 3600
    duration = max(duration, 0.01)
    price_per_hr = float(lot.price_per_hr)
    total_cost = round(duration * price_per_hr, 2)

    return render_template("user_release.html", res=res, date_time=release_time, total_cost=total_cost)
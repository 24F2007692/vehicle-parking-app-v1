from flask import request, redirect, url_for, flash, session,render_template
from app import app
from models.models import ParkingLot,db,ParkingSpot,Reservation

@app.route("/book_spot/<int:lot_id>", methods=['GET', 'POST'])
def book_spot(lot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    if request.method == 'POST':
        veh_no = request.form.get('veh_no')
        spot_id = request.form.get('spot_id')
        spot = ParkingSpot.query.get(spot_id)
        lot = ParkingLot.query.get(spot.lot_id)

        if spot and spot.status == 'A':
            spot.status = 'O'
            booking = Reservation(
                spot_id=spot.id, user_id=session['user_id'], vehicle_num=veh_no,address=lot.address)
            db.session.add(booking)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Spot is no longer available')
            return redirect(url_for('dashboard'))

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if spot:
        return render_template("user_booking.html", spot_id=spot.id, user_id=session['user_id'], lot_id=lot_id)
    else:
        flash("No available spots in this lot.")
        return redirect(url_for('dashboard'))
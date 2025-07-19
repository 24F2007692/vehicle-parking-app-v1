from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models.models import User, ParkingLot, ParkingSpot, Reservation


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.role == 'admin':
        lots = ParkingLot.query.all()
        spots = ParkingSpot.query.all()

        for lot in lots:
            lot.available_lots = ParkingSpot.query.filter_by(
                lot_id=lot.id, status='O').count()
        return render_template('admin_dashboard.html', lots=lots, spots=spots)
    else:
        # USER DASHBOARD - 1)SEARCH
        location = request.args.get('location')
        all_lots = []
        if location:
            pattern = f"%{location}%"
            all_lots = ParkingLot.query.filter(
                ParkingLot.address.ilike(pattern) |
                ParkingLot.prime_location_name.ilike(pattern) |
                ParkingLot.pincode.ilike(pattern)
            ).all()

        lots = []
        for lot in all_lots:
            lot.available_lots = ParkingSpot.query.filter_by(
                lot_id=lot.id, status='A').count()

            if lot.available_lots > 0:
                lots.append(lot)

        # USER DASHBOARD - 1)Fetch history
        reservations = Reservation.query.filter_by(user_id=session["user_id"]).all()
        
        history = []

        if reservations:
            for res in reservations:
                history.append([res.id, res.address, res.vehicle_num,
                               res.booking_time, res.Leaving_timestamp])

        return render_template("user_dashboard.html", lots=lots, location=location, history=history)
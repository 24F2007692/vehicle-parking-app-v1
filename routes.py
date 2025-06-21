from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import User, ParkingLot, ParkingSpot, Reservation, db
from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime, timezone


@app.route('/')
def index():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))
    return render_template("index.html", user=User.query.get(session['user_id']))


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.role == 'admin':
        lots = ParkingLot.query.all()
        spots = ParkingSpot.query.all()

        # OCCUPIED lots
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
        reserved = Reservation.query.filter_by(
            user_id=session["user_id"]).all()
        history = []

        for res in reserved:
            spot = ParkingSpot.query.get(res.spot_id)
            if spot:
                lot = ParkingLot.query.get(spot.lot_id)
                history.append([res.id, lot.address, res.vehicle_num,
                               res.booking_time, res.Leaving_timestamp, spot.id,])

        return render_template("user_dashboard.html")


# search functionality for ADMIN
@app.route("/search", methods=['GET', 'POST'])
def search():
    user = User.query.get(session['user_id'])
    if 'user_id' not in session and user.role != 'admin':
        flash('Please login to Continue')
        return redirect(url_for('login'))

    search_by = request.form.get('search_by')
    search_string = request.form.get('search_string')

    spots = ParkingSpot.query.all()
    all_lots = []
    if search_string:
        if search_by == 'location':
            pattern = f"%{search_string}%"
            all_lots = ParkingLot.query.filter(ParkingLot.address.ilike(
                pattern) | ParkingLot.prime_location_name.ilike(pattern)).all()

            # OCCUPIED lots
            for lot in all_lots:
                lot.available_lots = ParkingSpot.query.filter_by(
                    lot_id=lot.id, status='O').count()

            return render_template("admin_search.html", lots=all_lots, spots=spots, location=search_string)

        elif search_by == 'pincode':
            pincode = search_string
            all_lots = ParkingLot.query.filter(
                ParkingLot.pincode.ilike(pincode)).all()
            
            # OCCUPIED lots
            for lot in all_lots:
                lot.available_lots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()

            return render_template("admin_search.html", lots=all_lots, spots=spots, location=search_string)

        elif search_by == 'price_range':
            range1 = search_string.split('-')
            if len(range1) == 2:
                a = int(range1[0])
                b = int(range1[1])
                lots = []
                all_lots = ParkingLot.query.all()
                for lot in all_lots:
                    if a <= lot.price_per_hr <= b:
                        lots.append(lot)
                # OCCUPIED lots
                for lot in all_lots:
                    lot.available_lots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()

                return render_template("admin_search.html", lots=lots, spots=spots, location=f"price range {search_string}")
            else:
                message = "<h3>enter correct input like (20-30,200-300,400-500)<h3>"
                return render_template("admin_search.html", message=message)

    return render_template("admin_search.html")


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('mail')
    password = request.form.get('pass')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User does not exist")
        return redirect(url_for('login'))
    if not user.chk_pass(password):
        flash('Incorrect password')
        return redirect(url_for('login'))

    # Session
    session['user_id'] = user.id
    return redirect(url_for('dashboard'))


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('mail')
    password = request.form.get('pass')
    name = request.form.get('name')
    address = request.form.get('address')
    pincode = request.form.get('pincode')

    if User.query.filter_by(email=email).first():
        flash('user with this email already exists')
        return redirect(url_for('signup'))

    # add user if not in database
    user = User(email=email, password=password, name=name,
                address=address, pincode=pincode)

    db.session.add(user)
    db.session.commit()
    flash("User sucessfully registered")
    return redirect(url_for('dashboard'))


@app.route("/search_lot", methods=['POST'])
def search_lot():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))
    location = request.form.get('location')
    if location:
        return redirect(url_for('dashboard', location=location))
    return redirect(url_for('dashboard'))


# Logout and remove session
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)
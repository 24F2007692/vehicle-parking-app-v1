from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import User, ParkingLot, ParkingSpot, Reservation, db
from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime, timezone


@app.route('/')
def index():
    # if 'user_id' not in session:
    #     flash('Please login to Continue')
    #     return redirect(url_for('login'))
    # user=User.query.get(session['user_id'])
    return render_template("index.html", )


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

        return render_template("user_dashboard.html", lots=lots, location=location, history=history)


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


# ADMIN KE ROUTES

# FETCH USERS
@app.route('/allusers')
def allusers():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))
    users = User.query.all()
    data = [[user.id, user.email, user.name, user.address, user.pincode]
            for user in users]
    return render_template("admin_all_users.html", data=data)


# ADD A PARKING LOT
@app.route('/addlot', methods=['GET', 'POST'])
def addlot():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    if request.method == 'POST':
        location = request.form.get('location')
        price = request.form.get('price')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        max_spots = int(request.form.get('max_spots'))

        newlot = ParkingLot(prime_location_name=location, price_per_hr=price,
                            max_spots=max_spots, address=address, pincode=pincode)

        db.session.add(newlot)
        db.session.commit()
        flash("New lot added successfully")

    # add spots in parking lot:
        for i in range(1, max_spots+1):
            spot = ParkingSpot(lot_id=newlot.id, spot_no=i, status='A')
            db.session.add(spot)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("admin_new_parklot.html")


# EDIT A PARKING LOT (also changing spots acc to max_spots)
@app.route('/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    lot = ParkingLot.query.filter_by(id=lot_id).first()

    if request.method == 'POST':
        lot.prime_location_name = request.form.get('location')
        lot.price_per_hr = request.form.get('price')
        lot.address = request.form.get('address')
        lot.pincode = request.form.get('pincode')
        lot.max_spots = request.form.get('max_spots')

        # edit spots according to updated max_spots:
        reserved_spots = ParkingSpot.query.filter_by(
            lot_id=lot_id, status='O').all()
        for spot in reserved_spots:
            Reservation.query.filter_by(spot_id=spot.id).delete()
        ParkingSpot.query.filter_by(lot_id=lot_id).delete()

        for i in range(1, int(lot.max_spots)+1):
            spot = ParkingSpot(lot_id=lot_id, spot_no=i, status='A')
            db.session.add(spot)

        db.session.commit()
        flash("lot Updated successfully")
        return redirect(url_for('dashboard'))

    return render_template("admin_new_parklot.html", lot=lot)


# DELETE A PARKING LOT
@app.route('/del_lot/<int:lot_id>')
def del_lot(lot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        flash('Parking lot not found')
        return redirect(url_for('dashboard'))

    # delete reservation
    reserved_spots = ParkingSpot.query.filter_by(
        lot_id=lot_id, status='O').all()
    for spot in reserved_spots:
        Reservation.query.filter_by(spot_id=spot.id).delete()

    # delete spots of this lot
    ParkingSpot.query.filter_by(lot_id=lot_id).delete()

    # delete lot finally
    lot = ParkingLot.query.filter_by(id=lot_id).first()
    db.session.delete(lot)

    db.session.commit()
    flash("lot deleted successfully")
    return redirect(url_for('dashboard'))


# view parking spot details:
@app.route("/view_spot/<int:spot_id>", methods=["GET", "POST"])
def view_spot(spot_id):

    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    if not spot:
        flash("Spot not found")
        return redirect(url_for('dashboard'))

    return render_template("admin_parking_spot.html", status=spot.status, spot_id=spot_id)

# Occupied spot details
@app.route("/O_spot/<int:spot_id>")
def O_spot(spot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    O_spot = Reservation.query.filter_by(spot_id=spot_id).first()
    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    lot = ParkingLot.query.filter_by(id=spot.lot_id).first()

    if O_spot:
        booking_time = O_spot.booking_time.replace(tzinfo=timezone.utc)
        release_time = datetime.now(timezone.utc)
        duration = (release_time - booking_time).total_seconds() / 3600
        duration = max(duration, 0.01)
        price_per_hr = float(lot.price_per_hr)
        total_cost = round(duration * price_per_hr, 2)
        return render_template("admin_O_parking_details.html", O_spot=O_spot, total_cost=total_cost)

    return redirect(url_for('dashboard'))


# Delete a parking spot
@app.route("/del_spot/<int:spot_id>", methods=["GET", "POST"])
def del_spot(spot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    if not spot:
        flash("Spot not found")
        return redirect(url_for('dashboard'))

    # updating max_spots in ParkingLot table
    lot = ParkingLot.query.filter_by(id=spot.lot_id).first()

    # reservation bhi delete karni pdegi agar occupied delete kri to
    Reservation.query.filter_by(spot_id=spot_id).delete()

    db.session.delete(spot)
    if lot and lot.max_spots > 0:
        lot.max_spots -= 1
    db.session.commit()

    flash("Spot deleted successfully")
    return redirect(url_for('dashboard'))

# USER KI ROUTES

# Lot search
@app.route("/search_lot", methods=['POST'])
def search_lot():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))
    location = request.form.get('location')
    if location:
        return redirect(url_for('dashboard', location=location))
    return redirect(url_for('dashboard'))


# book parking spot in a lot
@app.route("/book_spot/<int:lot_id>", methods=['GET', 'POST'])
def book_spot(lot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    if request.method == 'POST':
        veh_no = request.form.get('veh_no')
        spot_id = request.form.get('spot_id')
        spot = ParkingSpot.query.get(spot_id)

        if spot and spot.status == 'A':
            spot.status = 'O'
            booking = Reservation(
                spot_id=spot.id, user_id=session['user_id'], vehicle_num=veh_no)
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


#Release a spot
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
        res.Leaving_timestamp = datetime.now(timezone.utc)
        spot.status = 'A'
        res.parking_cost = request.form.get("total_cost")
        db.session.commit()
        flash("Spot released successfully")
        return redirect(url_for('dashboard'))

    booking_time = res.booking_time.replace(tzinfo=timezone.utc)
    release_time = datetime.now(timezone.utc)

    duration = (release_time - booking_time).total_seconds() / 3600
    duration = max(duration, 0.01)
    price_per_hr = float(lot.price_per_hr)
    total_cost = round(duration * price_per_hr, 2)

    return render_template("user_release.html", res=res, date_time=release_time, total_cost=total_cost)



# Logout and remove session
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
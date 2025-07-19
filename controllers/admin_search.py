from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models.models import User, ParkingLot, ParkingSpot



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
                lot.available_lots = ParkingSpot.query.filter_by(
                    lot_id=lot.id, status='O').count()

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
                    lot.available_lots = ParkingSpot.query.filter_by(
                        lot_id=lot.id, status='O').count()

                return render_template("admin_search.html", lots=lots, spots=spots, location=f"price range {search_string}")
            else:
                message = "<h3>enter correct input like (20-30,200-300,400-500)<h3>"
                return render_template("admin_search.html", message=message)
        else:
            flash("Please select a valid search option")
            return redirect(url_for('search'))

    return render_template("admin_search.html")
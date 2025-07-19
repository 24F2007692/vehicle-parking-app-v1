from flask import request, redirect, url_for, flash, session,render_template
from app import app
from models.models import ParkingLot,db,ParkingSpot

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

        if max_spots > 1:
            newlot = ParkingLot(prime_location_name=location, price_per_hr=price,max_spots=max_spots, address=address, pincode=pincode)
            db.session.add(newlot)
            db.session.commit()
            flash("New lot added successfully")

            for i in range(1, max_spots+1):
                spot = ParkingSpot(lot_id=newlot.id, spot_no=i, status='A')
                db.session.add(spot)
            db.session.commit()
        else:
            flash("Please add at least 1 spot")
            return redirect(url_for('addlot'))
        
        return redirect(url_for('dashboard'))
    return render_template("admin_new_or_edit_parklot.html")
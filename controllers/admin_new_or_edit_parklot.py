from flask import request, redirect, url_for, flash, session,render_template
from app import app
from models.models import ParkingLot,db,ParkingSpot


@app.route('/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    if 'user_id' not in session:
        flash('Please login to continue')
        return redirect(url_for('login'))

    lot = ParkingLot.query.get(lot_id)

    if request.method == 'POST':
        new_max = int(request.form.get('max_spots'))
        if new_max <= 0:
            flash("Less than 1 spot is not allowed")
            return redirect(url_for('dashboard'))

        occupied_spots = ParkingSpot.query.filter_by(
            lot_id=lot_id, status='O').all()

        if len(occupied_spots) > new_max:
            flash("occupied spots cannot be less than new max spots")
            return redirect(url_for('dashboard'))


        fields = (lot.prime_location_name != request.form.get('location') or
                lot.price_per_hr != request.form.get('price') or
                lot.address != request.form.get('address') or
                lot.pincode != request.form.get('pincode'))
        
        lot.prime_location_name = request.form.get('location')
        lot.price_per_hr = request.form.get('price')
        lot.address = request.form.get('address')
        lot.pincode = request.form.get('pincode')

        old_max = lot.max_spots
        total_difference = new_max - old_max

        if total_difference > 0:
            for i in range(old_max + 1, new_max + 1):
                spot = ParkingSpot(lot_id=lot_id, spot_no=i, status='A')
                db.session.add(spot)
            lot.max_spots = new_max
            db.session.commit()
            flash("lot updated successfully")
            return redirect(url_for('dashboard'))


        elif total_difference < 0:
            available_spots = ParkingSpot.query.filter_by(
                lot_id=lot_id, status='A').all()

            for i in range(abs(total_difference)):
                db.session.delete(available_spots[i])
            lot.max_spots = new_max
            db.session.commit()
            flash("Lot updated successfully")
            return redirect(url_for('dashboard'))


        else:
            if fields:
                db.session.commit()
                flash("Lot updated successfully")
            else:
                flash("No changes detected")
                return redirect(url_for('dashboard'))

    return render_template("admin_new_or_edit_parklot.html", lot=lot)

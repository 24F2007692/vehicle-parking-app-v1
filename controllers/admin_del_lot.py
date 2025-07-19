from flask import redirect, url_for, flash, session
from app import app
from models.models import ParkingLot,db,ParkingSpot

@app.route('/del_lot/<int:lot_id>')
def del_lot(lot_id):
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    occupied_spots = ParkingSpot.query.filter_by(
        lot_id=lot_id, status='O').all()
    lot = ParkingLot.query.get(lot_id)


    if not lot or len(occupied_spots) > 0:
        flash('lot cannot be deleted')
        return redirect(url_for('dashboard'))

    ParkingSpot.query.filter_by(lot_id=lot_id).delete()

    lot = ParkingLot.query.filter_by(id=lot_id).first()
    db.session.delete(lot)

    db.session.commit()
    flash("lot deleted successfully")
    return redirect(url_for('dashboard'))
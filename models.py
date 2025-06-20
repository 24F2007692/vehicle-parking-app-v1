from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(32),unique=True,nullable=False)
    passhash = db.Column(db.String(512),nullable = False)
    name = db.Column(db.String(64),nullable=False)
    address = db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    role = db.Column(db.String(10),default = 'user',nullable=False)

    @property
    def password(self):
        raise AssertionError('password is not a readable Attribute')

    @password.setter
    def password(self,password):
        self.passhash= generate_password_hash(password)

    def chk_pass(self,password):
        return check_password_hash(self.passhash,password)

 
class ParkingLot(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    prime_location_name = db.Column(db.String(32),nullable=False)
    price_per_hr = db.Column(db.Float,nullable = False)
    address = db.Column(db.String(200),nullable=False)
    pincode = db.Column(db.String(10),nullable=False)
    max_spots = db.Column(db.Integer,nullable=False)

    spots = db.relationship('ParkingSpot',backref='lot',cascade='all,delete')
    

class ParkingSpot(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    lot_id = db.Column(db.Integer,db.ForeignKey('parking_lot.id'),nullable=False)
    spot_no = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(1),default='A')

    reservations = db.relationship('Reservation',backref='spot')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_time = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    Leaving_timestamp = db.Column(db.DateTime)
    parking_cost  = db.Column(db.Float)
    vehicle_num=db.Column(db.String(15))

    user = db.relationship('User', backref='reservations')



with app.app_context():
    db.create_all()
    
    #add admin if admin does't exist
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(email='admin@gmail.com',password='admin',name='admin',address='unknown',pincode='unknown',role='admin')
        db.session.add(admin)
        db.session.commit()
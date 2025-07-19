# controllers/admin_add_lot.py

# Zaroori modules import kiye ja rahe hain
from flask import request, redirect, url_for, flash, session,render_template
from app import app
from models.models import ParkingLot,db,ParkingSpot

# '/addlot' route, GET aur POST dono methods ke liye
@app.route('/addlot', methods=['GET', 'POST'])
def addlot():
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        # Agar nahi, toh login page par redirect karein
        flash('Please login to Continue') # "Login karna zaroori hai" flash message dikhaye
        return redirect(url_for('login'))

    # Agar request method POST hai
    if request.method == 'POST':
        # Form se data get karein
        location = request.form.get('location')
        price = request.form.get('price')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        max_spots = int(request.form.get('max_spots'))

        # Check karein ki max_spots 1 se zyada hai ya nahi
        if max_spots > 1:
            # Naya parking lot banayein
            newlot = ParkingLot(prime_location_name=location, price_per_hr=price,max_spots=max_spots, address=address, pincode=pincode)
            # Database session me naya lot add karein
            db.session.add(newlot)
            # Database me changes commit karein
            db.session.commit()
            # Success message flash karein
            flash("New lot added successfully") # "Naya lot safaltapoorvak joda gaya"

            # Jitne max_spots hain, utne parking spots banayein
            for i in range(1, max_spots+1):
                spot = ParkingSpot(lot_id=newlot.id, spot_no=i, status='A')
                db.session.add(spot)
            db.session.commit()
        else:
            # Agar max_spots 1 se kam hai, toh error flash karein
            flash("Please add at least 1 spot") # "Kripya kam se kam 1 spot jodein"
            return redirect(url_for('addlot'))
        
        # Dashboard par redirect karein
        return redirect(url_for('dashboard'))
    # Agar GET request hai, toh form render karein
    return render_template("admin_new_or_edit_parklot.html")

# controllers/admin_all_users.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template, redirect, url_for, flash, session
from app import app
from models.models import User

# '/allusers' route
@app.route('/allusers')
def allusers():
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        # Agar nahi, toh login page par redirect karein
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))
    # Sabhi users ko database se fetch karein
    users = User.query.all()
    # Users ka data ek list me store karein
    data = [[user.id, user.email, user.name, user.address, user.pincode]
            for user in users]
    # 'admin_all_users.html' template render karein aur data pass karein
    return render_template("admin_all_users.html", data=data)

# controllers/admin_del_lot.py

# Zaroori modules import kiye ja rahe hain
from flask import redirect, url_for, flash, session
from app import app
from models.models import ParkingLot,db,ParkingSpot

# '/del_lot/<int:lot_id>' route
@app.route('/del_lot/<int:lot_id>')
def del_lot(lot_id):
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))

    # Occupied spots ko filter karein
    occupied_spots = ParkingSpot.query.filter_by(
        lot_id=lot_id, status='O').all()
    # Lot ko ID se get karein
    lot = ParkingLot.query.get(lot_id)


    # Check karein ki lot exist karta hai ya nahi aur occupied spots hain ya nahi
    if not lot or len(occupied_spots) > 0:
        flash('lot cannot be deleted') # "Lot delete nahi kiya ja sakta"
        return redirect(url_for('dashboard'))

    # Lot se related parking spots delete karein
    ParkingSpot.query.filter_by(lot_id=lot_id).delete()

    # Lot ko delete karein
    lot = ParkingLot.query.filter_by(id=lot_id).first()
    db.session.delete(lot)

    # Database me changes commit karein
    db.session.commit()
    flash("lot deleted successfully") # "Lot safaltapoorvak delete kiya gaya"
    return redirect(url_for('dashboard'))

# controllers/admin_new_or_edit_parklot.py

# Zaroori modules import kiye ja rahe hain
from flask import request, redirect, url_for, flash, session,render_template
from app import app
from models.models import ParkingLot,db,ParkingSpot


# '/edit_lot/<int:lot_id>' route, GET aur POST dono methods ke liye
@app.route('/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # Lot ko ID se get karein
    lot = ParkingLot.query.get(lot_id)

    # Agar request method POST hai
    if request.method == 'POST':
        # Form se naye max spots get karein
        new_max = int(request.form.get('max_spots'))
        if new_max <= 0:
            flash("Less than 1 spot is not allowed") # "1 se kam spot anumati nahi hai"
            return redirect(url_for('dashboard'))

        # Occupied spots ko filter karein
        occupied_spots = ParkingSpot.query.filter_by(
            lot_id=lot_id, status='O').all()

        # Check karein ki occupied spots naye max spots se kam hain ya nahi
        if len(occupied_spots) > new_max:
            flash("occupied spots cannot be less than new max spots") # "Occupied spots naye max spots se kam nahi ho sakte"
            return redirect(url_for('dashboard'))


        # Form se lot details update karein
        lot.prime_location_name = request.form.get('location')
        lot.price_per_hr = request.form.get('price')
        lot.address = request.form.get('address')
        lot.pincode = request.form.get('pincode')

        # Purane aur naye max spots ka difference nikalein
        old_max = lot.max_spots
        total_difference = new_max - old_max

        # Agar naye spots add kiye gaye hain
        if total_difference > 0:
            for i in range(old_max + 1, new_max + 1):
                spot = ParkingSpot(lot_id=lot_id, spot_no=i, status='A')
                db.session.add(spot)
            lot.max_spots = new_max
            db.session.commit()
            flash("lot updated successfully") # "Lot safaltapoorvak update kiya gaya"
            return redirect(url_for('dashboard'))


        # Agar spots kam kiye gaye hain
        elif total_difference < 0:
            available_spots = ParkingSpot.query.filter_by(
                lot_id=lot_id, status='A').all()

            for i in range(abs(total_difference)):
                db.session.delete(available_spots[i])
            lot.max_spots = new_max
            db.session.commit()
            flash("Lot updated successfully") # "Lot safaltapoorvak update kiya gaya"
            return redirect(url_for('dashboard'))


        # Agar koi change nahi hua hai
        else:
            flash("No changes detected") # "Koi badlav nahi mila"
            return redirect(url_for('dashboard'))

    # Agar GET request hai, toh form render karein
    return render_template("admin_new_or_edit_parklot.html", lot=lot)

# controllers/admin_O_spot.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template, redirect, url_for, flash, session
from app import app
from models.models import ParkingLot,Reservation,ParkingSpot
from datetime import datetime, timezone,timedelta

# IST (Indian Standard Time) timezone set karein
IST = timezone(timedelta(hours=5, minutes=30))

# '/O_spot/<int:spot_id>' route
@app.route("/O_spot/<int:spot_id>")
def O_spot(spot_id):
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # Occupied spot ka reservation get karein
    O_spot = Reservation.query.filter_by(spot_id=spot_id).first()
    # Spot details get karein
    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    # Lot details get karein
    lot = ParkingLot.query.filter_by(id=spot.lot_id).first()

    # Agar spot occupied hai
    if O_spot:
        booking_time = O_spot.booking_time
        # Timezone information check karein
        if booking_time.tzinfo is None:
            booking_time = booking_time.replace(tzinfo=IST)
            curr_time = datetime.now(IST)
            # Parking duration calculate karein
            duration = (curr_time - booking_time).total_seconds() / 3600
            duration = max(duration, 0.01)
            price_per_hr = float(lot.price_per_hr)
            # Total cost calculate karein
            total_cost = round(duration * price_per_hr, 2)
        # Occupied spot details render karein
        return render_template("admin_O_spot.html", O_spot=O_spot, total_cost=total_cost,price_per_hr=round(price_per_hr),lot=lot)

    # Agar spot occupied nahi hai, toh dashboard par redirect karein
    return redirect(url_for('dashboard'))

# controllers/admin_search.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models.models import User, ParkingLot, ParkingSpot



# Admin ke liye search functionality
@app.route("/search", methods=['GET', 'POST'])
def search():
    # User get karein
    user = User.query.get(session['user_id'])
    # Check karein ki user logged in hai aur admin hai ya nahi
    if 'user_id' not in session and user.role != 'admin':
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # Form se search criteria get karein
    search_by = request.form.get('search_by')
    search_string = request.form.get('search_string')

    # Sabhi parking spots get karein
    spots = ParkingSpot.query.all()
    all_lots = []
    # Agar search string hai
    if search_string:
        # Agar location se search kiya gaya hai
        if search_by == 'location':
            pattern = f"%{search_string}%"
            all_lots = ParkingLot.query.filter(ParkingSpot.address.ilike(
                pattern) | ParkingLot.prime_location_name.ilike(pattern)).all()

            for lot in all_lots:
                lot.available_lots = ParkingSpot.query.filter_by(
                    lot_id=lot.id, status='O').count()

            return render_template("admin_search.html", lots=all_lots, spots=spots, location=search_string)

        # Agar pincode se search kiya gaya hai
        elif search_by == 'pincode':
            pincode = search_string
            all_lots = ParkingLot.query.filter(
                ParkingLot.pincode.ilike(pincode)).all()

            # OCCUPIED lots
            for lot in all_lots:
                lot.available_lots = ParkingSpot.query.filter_by(
                    lot_id=lot.id, status='O').count()

            return render_template("admin_search.html", lots=all_lots, spots=spots, location=search_string)

        # Agar price range se search kiya gaya hai
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
                message = "<h3>enter correct input like (20-30,200-300,400-500)<h3>" # "Sahi input format daalein"
                return render_template("admin_search.html", message=message)
        else:
            flash("Please select a valid search option") # "Kripya sahi search option chunein"
            return redirect(url_for('search'))

    return render_template("admin_search.html")

# controllers/admin_summary.py

# Zaroori modules import kiye ja rahe hain
from sqlalchemy import extract
import matplotlib.pyplot as plt
from flask import render_template, redirect, url_for, flash, session
from models.models import User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime
from app import app
import matplotlib
# Matplotlib ka backend set karein
matplotlib.use('Agg')


# '/summary' route
@app.route("/summary")
def summary():
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))
    
    # User get karein
    user = User.query.get(session['user_id'])

    # Check karein ki user admin hai ya nahi
    if user.role != 'admin':
        return redirect(url_for('login'))


    # Total users count karein
    total_users = User.query.filter(User.role == "user").count()

    # Current month get karein
    current_month = datetime.now().strftime("%m")

    now = datetime.now()
    # Is mahine ki bookings get karein
    bookings = Reservation.query.filter(
        Reservation.Leaving_timestamp != None,extract('month', Reservation.Leaving_timestamp) == now.month,extract('year', Reservation.Leaving_timestamp) == now.year).all()

    # Is mahine ka revenue calculate karein
    revenue_this_month = 0
    for res in bookings:
        revenue_this_month += res.parking_cost

    # Available spots count karein
    Available_spots = ParkingSpot.query.filter(
        ParkingSpot.status == 'A').count()

    # Occupied spots count karein
    occupied_spots = ParkingSpot.query.filter(
        ParkingSpot.status == 'O').count()

    # Total lots count karein
    total_lots = ParkingLot.query.count()


    # Pie chart ke liye labels
    pie_labels = ['Available spots', 'Occupied spots']
    plt.clf()
    # Agar spots hain
    if (Available_spots + occupied_spots) > 0:
        print(True)
        # Pie chart banayein
        plt.pie([Available_spots,occupied_spots], labels=pie_labels, colors=["#00ff15", "#ff0000"], autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Reservation Status Distribution") # "Reservation sthiti vitran"
        # Chart ko image file me save karein
        plt.savefig("static/images/pie2.png", transparent=True)



    # Monthly revenue ke liye data prepare karein
    res_list = Reservation.query.filter(Reservation.parking_cost != None).all()
    monthly_revenue = {}
    for res in res_list:
        if res.Leaving_timestamp:
            key = res.Leaving_timestamp.strftime('%Y-%m')
            if key not in monthly_revenue:
                monthly_revenue[key] = 0
            monthly_revenue[key] += res.parking_cost
    
    # print(monthly_revenue)  # : {'2025-07': 255898.76999999996}

    # Mahine aur amount sort karein
    months = sorted(monthly_revenue.keys())
    amounts = [monthly_revenue[m] for m in months]


    plt.clf()
    # Agar 8 se zyada mahine hain
    if len(months) > 8:
        plt.clf()
        # Line plot banayein
        plt.plot(months, amounts, marker='o', color='#e67e22')
        plt.xlabel("Month") # "Mahina"
        plt.ylabel("Total Revenue (₹)") # "Kul aay"
        plt.title("Parking Revenue Over Time (All Users)") # "Parking aay samay ke saath"
        plt.grid()
        plt.tight_layout()
        # Chart ko image file me save karein
        plt.savefig('static/images/hist2.png', transparent=True)
        
    # Summary template render karein
    return render_template("admin_summary.html", total_users=total_users, revenue_this_month=f"₹{revenue_this_month:,.2f}", Available_spots=Available_spots, occupied_spots=occupied_spots, total_lots=total_lots, total_spots=Available_spots+occupied_spots)

# controllers/admin_view_spot.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template, redirect, url_for, flash, session
from app import app
from models.models import ParkingSpot

# '/view_spot/<int:spot_id>' route
@app.route("/view_spot/<int:spot_id>", methods=["GET", "POST"])
def view_spot(spot_id):

    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # Spot ko ID se get karein
    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    # Agar spot nahi milta hai
    if not spot:
        flash("Spot not found") # "Spot nahi mila"
        return redirect(url_for('dashboard'))

    # Spot view template render karein
    return render_template("admin_view_spot.html", status=spot.status, spot_no=spot.spot_no, spot_id=spot.id)

# controllers/dashboard.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models.models import User, ParkingLot, ParkingSpot, Reservation


# '/dashboard' route
@app.route('/dashboard')
def dashboard():
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # User get karein
    user = User.query.get(session['user_id'])

    # Agar user admin hai
    if user.role == 'admin':
        # Sabhi lots aur spots get karein
        lots = ParkingLot.query.all()
        spots = ParkingSpot.query.all()

        # Har lot ke liye available spots count karein
        for lot in lots:
            lot.available_lots = ParkingSpot.query.filter_by(
                lot_id=lot.id, status='O').count()
        # Admin dashboard render karein
        return render_template('admin_dashboard.html', lots=lots, spots=spots)
    else:
        # USER DASHBOARD - 1)SEARCH
        # Location get karein
        location = request.args.get('location')
        all_lots = []
        # Agar location hai, toh search karein
        if location:
            pattern = f"%{location}%"
            all_lots = ParkingLot.query.filter(
                ParkingLot.address.ilike(pattern) |
                ParkingLot.prime_location_name.ilike(pattern) |
                ParkingLot.pincode.ilike(pattern)
            ).all()

        lots = []
        for lot in all_lots:
            # Available spots count karein
            lot.available_lots = ParkingSpot.query.filter_by(
                lot_id=lot.id, status='A').count()

            if lot.available_lots > 0:
                lots.append(lot)

        # USER DASHBOARD - 1)Fetch history
        # User ki reservations fetch karein
        reservations = Reservation.query.filter_by(user_id=session["user_id"]).all()
        
        history = []

        # Agar reservations hain
        if reservations:
            for res in reservations:
                history.append([res.id, res.address, res.vehicle_num,
                               res.booking_time, res.Leaving_timestamp])

        # User dashboard render karein
        return render_template("user_dashboard.html", lots=lots, location=location, history=history)

# controllers/edit_profile.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template, request, redirect, url_for, flash, session
from models.models import User, db
from app import app


# '/editprofile' route, GET aur POST dono methods ke liye
@app.route("/editprofile", methods=["GET", "POST"])
def editprofile():
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # User get karein
    user = User.query.get(session['user_id'])

    # Agar request method POST hai
    if request.method == "POST":
        # Form se old aur new password get karein
        old_pass = request.form.get('O_pass')
        new_pass = request.form.get('N_pass')

        # Agar old password nahi daala hai
        if not old_pass:
            flash('Please enter your old password to update your profile') # "Profile update karne ke liye purana password daalein"
            return redirect(url_for('editprofile'))

        # Agar old password galat hai
        if not user.chk_pass(old_pass):
            flash('Old password is incorrect') # "Purana password galat hai"
            return redirect(url_for('editprofile'))

        # Form se nayi details get karein
        new_name = request.form.get('name')
        new_address = request.form.get('address')
        new_pincode = request.form.get('pincode')

        # Agar koi field khali hai
        if not new_name or not new_address or not new_pincode:
            flash('do not leave any field empty') # "Koi bhi field khali na chhodein"
            return redirect(url_for('editprofile'))


        is_changed = False

        # Agar naam badla hai
        if new_name != user.name:
            user.name = new_name
            is_changed = True

        # Agar address badla hai
        if new_address != user.address:
            user.address = new_address
            is_changed = True

        # Agar pincode badla hai
        if new_pincode != user.pincode:
            user.pincode = new_pincode
            is_changed = True

        # Agar password badla hai
        if new_pass:
            user.password = new_pass
            is_changed = True

        # Agar koi badlav hua hai
        if is_changed:
            db.session.commit()
            flash('Profile updated successfully') # "Profile safaltapoorvak update ho gayi"
        else:
            flash('No changes detected') # "Koi badlav nahi mila"

        # Session me naya naam update karein
        session['user_name'] = user.name
        # Dashboard par redirect karein
        return redirect(url_for('dashboard'))

    # Agar GET request hai, toh edit profile page render karein
    return render_template("edit_profile.html", user=user)

# controllers/index.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template
from app import app

# '/' (home) route
@app.route('/')
def index():
    # 'index.html' template render karein
    return render_template("index.html")

# controllers/login.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template,redirect,request,url_for,flash,session
from app import app
from models.models import User

# '/login' route
@app.route('/login')
def login():
    # 'login.html' template render karein
    return render_template("login.html")

# '/login' route, POST method ke liye
@app.route('/login', methods=['POST'])
def login_post():
    # Form se email aur password get karein
    email = request.form.get('mail')
    password = request.form.get('pass')

    # Agar email aur password khali nahi hain
    if email != "" and password != "":
        # User ko email se filter karein
        user = User.query.filter_by(email=email).first()

        # Agar user exist nahi karta
        if not user:
            flash("User does not exist") # "User maujood nahi hai"
            return redirect(url_for('login'))
        
        # Agar password galat hai
        if not user.chk_pass(password):
            flash('Incorrect password') # "Galat password"
            return redirect(url_for('login'))
        # Session me user ID aur naam set karein
        session['user_id'] = user.id
        session['user_name'] = user.name
    else:
        # Agar koi field khali hai
        flash('mat kar lala mat kar!!') # "Mat kar lala mat kar!!"
        return redirect(url_for('login'))
    # Welcome message flash karein
    flash(f"welcome {user.role}") # "Swagat hai"
    # Dashboard par redirect karein
    return redirect(url_for('dashboard'))

# controllers/logout.py

# Zaroori modules import kiye ja rahe hain
from flask import redirect, url_for, session
from app import app


# Logout and remove session
@app.route('/logout')
def logout():
    # Session se user ID remove karein
    session.pop('user_id', None)
    # Login page par redirect karein
    return redirect(url_for('login'))

# controllers/signup.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template,redirect,request,url_for,flash,session
from app import app
from models.models import User,db

# '/signup' route
@app.route('/signup')
def signup():
    # 'signup.html' template render karein
    return render_template("signup.html")


# '/signup' route, POST method ke liye
@app.route('/signup', methods=['POST'])
def signup_post():
    # Form se data get karein
    email = request.form.get('mail')
    password = request.form.get('pass')
    name = request.form.get('name')
    address = request.form.get('address')
    pincode = request.form.get('pincode')

    # Agar sabhi details bhari hain
    if email != "" and password != "" and name != "" and address != "" and pincode != "":
        # Naya user banayein
        user = User(email=email, password=password, name=name,address=address, pincode=pincode)

        # Check karein ki user pehle se exist karta hai ya nahi
        if User.query.filter_by(email=email).first():
            flash('user with this email already exists') # "Is email ke saath user pehle se maujood hai"
            return redirect(url_for('signup'))
    
    else:
        # Agar sabhi details nahi bhari hain
        flash('Enter all details') # "Sabhi vivaran daalein"
        return redirect(url_for('signup'))

    # Naye user ko database session me add karein
    db.session.add(user)
    # Database me changes commit karein
    db.session.commit()
    # Session me user ID aur naam set karein
    session['user_id'] = user.id
    session['user_name'] = user.name
    # Success message flash karein
    flash("User sucessfully registered") # "User safaltapoorvak panjeekrt ho gaya"
    # Dashboard par redirect karein
    return redirect(url_for('dashboard'))

# controllers/user_book_spot.py

# Zaroori modules import kiye ja rahe hain
from flask import request, redirect, url_for, flash, session,render_template
from app import app
from models.models import ParkingLot,db,ParkingSpot,Reservation

# '/book_spot/<int:lot_id>' route, GET aur POST dono methods ke liye
@app.route("/book_spot/<int:lot_id>", methods=['GET', 'POST'])
def book_spot(lot_id):
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # Agar request method POST hai
    if request.method == 'POST':
        # Form se vehicle number aur spot ID get karein
        veh_no = request.form.get('veh_no')
        spot_id = request.form.get('spot_id')
        # Spot aur lot get karein
        spot = ParkingSpot.query.get(spot_id)
        lot = ParkingLot.query.get(spot.lot_id)

        # Agar spot available hai
        if spot and spot.status == 'A':
            # Spot ka status 'Occupied' set karein
            spot.status = 'O'
            # Nayi booking banayein
            booking = Reservation(
                spot_id=spot.id, user_id=session['user_id'], vehicle_num=veh_no,address=lot.address)
            # Booking ko database session me add karein
            db.session.add(booking)
            # Database me changes commit karein
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            # Agar spot available nahi hai
            flash('Spot is no longer available') # "Spot ab uplabdh nahi hai"
            return redirect(url_for('dashboard'))

    # Agar GET request hai, toh available spot dhoondein
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    # Agar spot milta hai
    if spot:
        # Booking page render karein
        return render_template("user_booking.html", spot_id=spot.id, user_id=session['user_id'], lot_id=lot_id)
    else:
        # Agar koi spot available nahi hai
        flash("No available spots in this lot.") # "Is lot me koi spot uplabdh nahi hai"
        return redirect(url_for('dashboard'))

# controllers/user_release_spot.py

# Zaroori modules import kiye ja rahe hain
from flask import request,render_template, redirect, url_for, flash, session
from models.models import  ParkingLot, ParkingSpot, Reservation, db
from datetime import datetime, timezone, timedelta
from app import app


# IST timezone set karein
IST = timezone(timedelta(hours=5, minutes=30))



# '/release/<int:res_id>' route, GET aur POST dono methods ke liye
@app.route("/release/<int:res_id>", methods=['GET', 'POST'])
def release(res_id):
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # Reservation get karein
    res = Reservation.query.get(res_id)
    # Agar reservation nahi milta hai
    if not res:
        flash("Reservation not found") # "Reservation nahi mila"
        return redirect(url_for('dashboard'))

    # Spot aur lot get karein
    spot = ParkingSpot.query.get(res.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)

    # Agar request method POST hai
    if request.method == 'POST':
        # Leaving timestamp set karein
        res.Leaving_timestamp = datetime.now(IST)
        # Spot ka status 'Available' set karein
        spot.status = 'A'
        # Parking cost set karein
        res.parking_cost = request.form.get("total_cost")
        res.spot_id = None
        # Database me changes commit karein
        db.session.commit()
        flash("Spot released successfully") # "Spot safaltapoorvak chhod diya gaya"
        return redirect(url_for('dashboard'))

    # Booking time get karein
    booking_time = res.booking_time
    if booking_time.tzinfo is None:
        booking_time = booking_time.replace(tzinfo=IST)
    # Release time get karein
    release_time = datetime.now(IST)


    # Parking duration aur total cost calculate karein
    duration = (release_time - booking_time).total_seconds() / 3600
    duration = max(duration, 0.01)
    price_per_hr = float(lot.price_per_hr)
    total_cost = round(duration * price_per_hr, 2)

    # Release page render karein
    return render_template("user_release.html", res=res, date_time=release_time, total_cost=total_cost)

# controllers/user_search_lot.py

# Zaroori modules import kiye ja rahe hain
from flask import request, redirect, url_for, flash, session
from app import app

# '/search_lot' route, POST method ke liye
@app.route("/search_lot", methods=['POST'])
def search_lot():
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))

    # Form se location get karein
    location = request.form.get('location')

    # Agar location hai
    if location:
        # Dashboard par location ke saath redirect karein
        return redirect(url_for('dashboard', location=location))
    else:
        # Agar location nahi hai
        flash("Please enter a valid location") # "Kripya ek vaidh sthan daalein"
        
    # Dashboard par redirect karein
    return redirect(url_for('dashboard'))

# controllers/user_summary.py

# Zaroori modules import kiye ja rahe hain
from flask import render_template, redirect, url_for, flash, session
from models.models import User,Reservation
from datetime import timezone, timedelta
from app import app
import matplotlib
# Matplotlib ka backend set karein
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# IST timezone set karein
IST = timezone(timedelta(hours=5, minutes=30))

# '/usersummary' route
@app.route("/usersummary")
def usersummary():
    
    # Check karein ki user logged in hai ya nahi
    if 'user_id' not in session:
        flash('Please login to Continue') # "Login karna zaroori hai"
        return redirect(url_for('login'))
    # User get karein
    user = User.query.get(session['user_id'])


    # Active, total aur released bookings get karein
    active_bookings = Reservation.query.filter_by(parking_cost=None, user_id=user.id)
    total_bookings = Reservation.query.filter_by(user_id=user.id).count()
    released_reservations = Reservation.query.filter(Reservation.parking_cost != None, Reservation.user_id == user.id)

    # Total amount spent aur parking durations calculate karein
    total_amount_spent = 0
    durations = []
    for res in released_reservations:
        total_amount_spent += res.parking_cost
        booking_time = res.booking_time
        release_time = res.Leaving_timestamp
        if not release_time:
            continue
        if booking_time.tzinfo is None:
            booking_time = booking_time.replace(tzinfo=IST)
        if release_time.tzinfo is None:
            release_time = release_time.replace(tzinfo=IST)
        duration = max((release_time - booking_time).total_seconds() / 3600, 0)
        durations.append(duration)

    # Average parking duration calculate karein
    if durations:
        avg_parking_duration = round(sum(durations) / len(durations), 2)
        hours = int(avg_parking_duration)
        minutes = int((avg_parking_duration - hours) * 60)
        formatted_avg_duration = f"{hours} hr {minutes} min"
    else:
        formatted_avg_duration = 0



    # Histogram ke liye bins aur labels
    bins = [0, 1, 2, 3, 4, 5, 6,24]
    labels = ["<1 hr", "1-2 hr", "2-3 hr", "3-4 hr", "4-5 hr", "5-6 hr", ">6 hr"]

    # Counts calculate karein
    counts = [0] * (len(bins) - 1)
    for d in durations:
        for i in range(len(bins) - 1):
            print(bins[i],bins[i+1],d)
            if bins[i] <= d < bins[i + 1]:
                counts[i] += 1
                break
            else:
                counts[-1] += 1

    # print(counts)            
    plt.clf()
    # Agar 8 se zyada counts hain
    if sum(counts) > 8:   
        # Bar chart banayein
        plt.bar(labels, counts)
        plt.xlabel("Duration") # "Avadhi"
        plt.ylabel("Reserv. Cnt") # "Reservation Ginti"
        plt.title("Parking Duration Distribution") # "Parking avadhi vitran"
        plt.tight_layout()
        # Chart ko image file me save karein
        plt.savefig("static/images/hist1.png", transparent=True)
        


    # Pie chart ke liye data
    active_count = active_bookings.count()
    completed_count = released_reservations.count()
    pie_labels = ['Active', 'Completed']
    sizes = [active_count, completed_count]
    colors = ['#3498db', '#2ecc71']

    plt.clf()
    # Agar bookings hain
    if active_count + completed_count > 0:
        # Pie chart banayein
        plt.pie(sizes, labels=pie_labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Reservation Status Distribution") # "Reservation sthiti vitran"
        # Chart ko image file me save karein
        plt.savefig("static/images/pie1.png", transparent=True)

    # User summary template render karein
    return render_template(
        "user_summary.html",
        active_bookings=int(active_count),
        total_bookings=int(total_bookings),
        total_amount_spent=f"₹{total_amount_spent:,.2f}",
        formatted_avg_duration=formatted_avg_duration
    )
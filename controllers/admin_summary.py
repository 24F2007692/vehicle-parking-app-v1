from sqlalchemy import extract
import matplotlib.pyplot as plt
from flask import render_template, redirect, url_for, flash, session
from models.models import User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime
from app import app
import matplotlib
matplotlib.use('Agg')


@app.route("/summary")
def summary():
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])

    if user.role != 'admin':
        return redirect(url_for('login'))


    total_users = User.query.filter(User.role == "user").count()

    current_month = datetime.now().strftime("%m")

    now = datetime.now()
    bookings = Reservation.query.filter(
        Reservation.Leaving_timestamp != None,extract('month', Reservation.Leaving_timestamp) == now.month,extract('year', Reservation.Leaving_timestamp) == now.year).all()

    revenue_this_month = 0
    for res in bookings:
        revenue_this_month += res.parking_cost

    Available_spots = ParkingSpot.query.filter(
        ParkingSpot.status == 'A').count()

    occupied_spots = ParkingSpot.query.filter(
        ParkingSpot.status == 'O').count()

    total_lots = ParkingLot.query.count()


    pie_labels = ['Available spots', 'Occupied spots']
    plt.clf()
    if (Available_spots + occupied_spots) > 0:
        print(True)
        plt.pie([Available_spots,occupied_spots], labels=pie_labels, colors=["#00ff15", "#ff0000"], autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Reservation Status Distribution")
        plt.savefig("static/images/pie2.png", transparent=True)



    res_list = Reservation.query.filter(Reservation.parking_cost != None).all()
    monthly_revenue = {}
    for res in res_list:
        if res.Leaving_timestamp:
            key = res.Leaving_timestamp.strftime('%Y-%m')
            if key not in monthly_revenue:
                monthly_revenue[key] = 0
            monthly_revenue[key] += res.parking_cost
    
    # print(monthly_revenue)  # : {'2025-07': 255898.76999999996}

    months = sorted(monthly_revenue.keys())
    amounts = [monthly_revenue[m] for m in months]


    plt.clf()
    if len(months) > 8:
        plt.clf()
        plt.plot(months, amounts, marker='o', color='#e67e22')
        plt.xlabel("Month")
        plt.ylabel("Total Revenue (₹)")
        plt.title("Parking Revenue Over Time (All Users)")
        plt.grid()
        plt.tight_layout()
        plt.savefig('static/images/hist2.png', transparent=True)
        
    return render_template("admin_summary.html", total_users=total_users, revenue_this_month=f"₹{revenue_this_month:,.2f}", Available_spots=Available_spots, occupied_spots=occupied_spots, total_lots=total_lots, total_spots=Available_spots+occupied_spots)

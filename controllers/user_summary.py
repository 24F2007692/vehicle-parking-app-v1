from flask import render_template, redirect, url_for, flash, session
from models.models import User,Reservation
from datetime import timezone, timedelta
from app import app
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

IST = timezone(timedelta(hours=5, minutes=30))

@app.route("/usersummary")
def usersummary():
    
    if 'user_id' not in session:
        flash('Please login to Continue')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])


    active_bookings = Reservation.query.filter_by(parking_cost=None, user_id=user.id)
    total_bookings = Reservation.query.filter_by(user_id=user.id).count()
    released_reservations = Reservation.query.filter(Reservation.parking_cost != None, Reservation.user_id == user.id)

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

    if durations:
        avg_parking_duration = round(sum(durations) / len(durations), 2)
        hours = int(avg_parking_duration)
        minutes = int((avg_parking_duration - hours) * 60)
        formatted_avg_duration = f"{hours} hr {minutes} min"
    else:
        formatted_avg_duration = 0



    bins = [0, 1, 2, 3, 4, 5, 6,24]
    labels = ["<1 hr", "1-2 hr", "2-3 hr", "3-4 hr", "4-5 hr", "5-6 hr", ">6 hr"]

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
    if sum(counts) > 8:   
        plt.bar(labels, counts)
        plt.xlabel("Duration")
        plt.ylabel("Reserv. Cnt")
        plt.title("Parking Duration Distribution")
        plt.tight_layout()
        plt.savefig("static/images/hist1.png", transparent=True)
        



    active_count = active_bookings.count()
    completed_count = released_reservations.count()
    pie_labels = ['Active', 'Completed']
    sizes = [active_count, completed_count]
    colors = ['#3498db', '#2ecc71']

    plt.clf()
    if active_count + completed_count > 0:
        plt.pie(sizes, labels=pie_labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Reservation Status Distribution")
        plt.savefig("static/images/pie1.png", transparent=True)

    return render_template(
        "user_summary.html",
        active_bookings=int(active_count),
        total_bookings=int(total_bookings),
        total_amount_spent=f"₹{total_amount_spent:,.2f}",
        formatted_avg_duration=formatted_avg_duration
    )





 




# SmartParkr: Vehicle Parking Management App

SmartParkr is a multi-user web application for managing 4-wheeler parking lots, spots, and reservations. It supports both admin and regular user roles, providing dashboards, statistics, and a smooth booking experience.

## Features

### For Users
- **Signup/Login/Logout**: Secure authentication and session management.
- **Search Parking Lots**: Find lots by location or pincode.
- **Book a Spot**: Reserve available spots in any lot.
- **Release a Spot**: End your reservation and calculate cost based on duration.
- **View Booking History**: See all past and active reservations.
- **Profile Management**: Edit your name, address, pincode, and password.
- **Personal Statistics**: Visualize your parking durations and spending.

### For Admins
- **Dashboard Overview**: View all lots, spots, and their statuses.
- **Add/Edit/Delete Lots**: Manage parking lots and their capacities.
- **View All Users**: List and review registered users.
- **Search Lots/Spots**: Filter by location, pincode, or price range.
- **Spot Management**: View details of any spot, including occupancy and cost.
- **Statistics & Revenue**: See monthly revenue, spot utilization, and user stats with charts.

## Data Model Overview
- **User**: email, password (hashed), name, address, pincode, role (admin/user)
- **ParkingLot**: location name, address, pincode, price per hour, max spots
- **ParkingSpot**: spot number, lot reference, status (Available/Occupied)
- **Reservation**: user, spot, vehicle number, booking time, leaving time, cost

## Visualizations
- **Pie Charts**: Show active vs. completed bookings, and spot availability.
- **Bar/Line Charts**: Show parking duration distribution and monthly revenue (admin).
- Charts are auto-generated and saved in `static/images/`.

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone [<repo-url>](https://github.com/24F2007692/vehicle-parking-app-v1)
   cd parking_app_24F2007692
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app**
   ```bash
   python app.py
   ```
   The app uses SQLite by default (`db.sqlite3`).

4. **Configuration**
   - Edit `config.py` for DB URI or secret key if needed.
   - Environment variables: `SECRET_KEY`, `TRACK_MODIFICATIONS` (optional).

5. **Access**
   - Open [http://localhost:5000](http://localhost:5000) in your browser.
   - Default admin: `admin@gmail.com` / `admin` (created automatically if not present).

## Usage

- **Signup**: Register as a new user.
- **Login**: Use your credentials to access the dashboard.
- **Admin**: Log in with the admin account for management features.
- **Book/Release**: Users can book and release spots from their dashboard.
- **Edit Profile**: Update your details and password securely.

## Project Structure

```
The project is organized into a modular structure to keep the code clean and maintainable.
/parking_app
|
|-- app.py                  # Main Flask application file, initializes the app and extensions.
|-- config.py               # Configuration settings for the application.
|-- models/
|   |-- models.py           # Defines the database schema (User, ParkingLot, etc.).
|
|-- controllers/
|   |-- admin_*.py          # Route handlers for all admin functionalities.
|   |-- user_*.py           # Route handlers for all user functionalities.
|   |-- login.py, etc.      # Handlers for auth, dashboard, and other general routes.
|
|-- templates/
|   |-- admin_*.html        # HTML templates for the admin interface.
|   |-- user_*.html         # HTML templates for the user interface.
|   |-- login.html, etc.    # General HTML templates.
|
|-- static/
|   |-- css/                # CSS stylesheets.
|   |-- js/                 # JavaScript files.
|   |-- images/             # Static images and generated charts.
|
|-- instance/
|   |-- db.sqlite3          # The SQLite database file.
|
|-- requirements.txt        # Lists all Python dependencies.
|-- README.md               # This file.
```

## Customization
- **Styling**: Edit files in `static/css/` for custom look and feel.
- **Templates**: Modify HTML in `templates/` for UI changes.
- **Charts**: Generated with Matplotlib, saved in `static/images/`.

## License
OPEN
**For any issues or contributions, please open an issue or pull request.**

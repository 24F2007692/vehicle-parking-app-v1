🚗 Smart Parking Management SystemA comprehensive web application built with Flask for managing parking lots. This system provides a seamless experience for both users looking for a parking spot and administrators managing the facilities. It features separate dashboards for users and admins, each tailored with specific functionalities.✨ FeaturesFor Users 🙋‍♂️Authentication: Secure user registration and login system.Profile Management: Users can view and update their personal information.Search Functionality: Easily search for available parking lots by location, address, or pincode.Real-Time Booking: Book an available parking spot in a chosen lot.Spot Release: Release a booked spot, with automatic calculation of parking duration and cost.Personal Dashboard: View current active bookings and a complete history of past reservations.Usage Summary: A personalized summary page with visualizations showing booking statistics, total amount spent, and average parking duration.For Admins 👨‍💼Admin Dashboard: An overview of all parking lots, their status, and the number of occupied spots.Lot Management: Admins can add, edit, or delete entire parking lots.Spot Management: View the status of every spot within a lot (Available/Occupied).User Management: View a list of all registered users and their details.Detailed Search: Advanced search for lots based on location, pincode, or price range.Occupancy Details: Get detailed information for any occupied spot, including the user who booked it and the total cost incurred so far.System Summary: A comprehensive summary page with key metrics like total users, monthly revenue, and overall spot occupancy, complete with graphical charts.🛠️ Tech StackBackend: Python, FlaskDatabase: Flask-SQLAlchemy (with SQLite as the database engine)Frontend: HTML, CSS, JavaScriptData Visualization: Matplotlib (for generating summary charts)Server: Werkzeug (Flask's development server)📂 Project StructureThe project is organized into a modular structure to keep the code clean and maintainable./parking_app
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
🚀 Setup and InstallationFollow these steps to get the project running on your local machine.1. Clone the Repositorygit clone <your-repository-url>
cd parking_app_24F2007692
2. Create and Activate a Virtual EnvironmentIt's highly recommended to use a virtual environment to manage project dependencies.On macOS/Linux:python3 -m venv venv
source venv/bin/activate
On Windows:python -m venv venv
.\venv\Scripts\activate
3. Install DependenciesCreate a requirements.txt file with the following content:Flask
Flask-SQLAlchemy
matplotlib
Then, install all the necessary packages using pip:pip install -r requirements.txt
4. Configure the Flask AppThe application needs to know which file to run. Set the FLASK_APP environment variable.On macOS/Linux:export FLASK_APP=app.py
On Windows (Command Prompt):set FLASK_APP=app.py
On Windows (PowerShell):$env:FLASK_APP="app.py"
5. Run the ApplicationNow, you can start the Flask development server:flask run
The application will be running at http://127.0.0.1:5000. Open this URL in your web browser to use the app.📖 UsageAdmin Account: To access the admin panel, you may need to manually change a user's role to admin in the db.sqlite3 database file.User Account: Simply sign up as a new user to access the user dashboard and features.This README was generated with assistance from Google's Gemini.

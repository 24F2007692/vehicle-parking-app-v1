from flask import redirect, url_for, session
from app import app


# Logout and remove session
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
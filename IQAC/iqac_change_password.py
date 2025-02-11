from flask import Blueprint, render_template, request, redirect, url_for, session
from database import DBSession , IQAC_C0

iqac_change_password_bp = Blueprint('iqac_change_password', __name__)

# Route for displaying and handling the password change form
@iqac_change_password_bp.route('/iqac_change_password', methods=['GET', 'POST'])
def iqac_change_password():
    if 'username' not in session:
        # Redirect to login page if user is not logged in
        return render_template('index.html', message="You are not logged in")
    
    iqacemail=session['username']
           
    dbsession = DBSession()
    iqac_entry = dbsession.query(IQAC_C0).filter_by(emailid=iqacemail).first()

    if iqac_entry:
        existing_password = iqac_entry.password
    else:
        existing_password = None
        dbsession.close()

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        # Retrieve iqac from database (you may want to add more robust error handling here)
        dbsession = DBSession()
        iqac = dbsession.query(IQAC_C0).filter_by(emailid=iqacemail).first()

        # Check if current password matches the one in the database
        if current_password == iqac.password:
            # Check if new password and confirmed password match
            if new_password == confirm_new_password:
                # Update password in the database
                iqac.password = new_password
                dbsession.commit()
                dbsession.close()
                return render_template('iqac/dashboard.html' , messages ="Your Password is Sucessfuly Changed")
            else:
                # Handle case where current password is incorrect
                return render_template('iqac/change_password.html', error="New password and confirmed password don't match",existing_password = existing_password)
        else:
            return render_template('iqac/change_password.html', error="Current password is incorrect",existing_password = existing_password)
    else:
        return render_template('iqac/change_password.html', existing_password=existing_password)
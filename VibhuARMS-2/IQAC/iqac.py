from flask import Blueprint, render_template, request,session
iqac_bp = Blueprint('iqac', __name__)
from database import IQAC_C0, DBSession

@iqac_bp.route('/iqac_dashboard', methods=['GET', 'POST'])
def iqac_dashboard():
    if request.method == 'POST':
        iqacemail = request.form['iqacemail']
        password = request.form['iqacpassword']
        
        # Query the database to check if the user exists
        dbsession = DBSession()
        user = dbsession.query(IQAC_C0).filter(IQAC_C0.emailid == iqacemail, IQAC_C0.password == password).first()
        dbsession.close()
        
        if user:
            session['username'] = user.name
            return render_template('iqac/dashboard.html', username=session['username'])
        else:
            return render_template('index.html', message="Invalid username or Password")
    
    if 'username' not in session:
        return render_template('index.html',message="You are not LoggedIn")
    else:
        return render_template('iqac/dashboard.html')

@iqac_bp.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')
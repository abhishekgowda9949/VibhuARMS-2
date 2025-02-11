from flask import Blueprint, render_template, request, session
from database import DBSession, Employee

user_bp = Blueprint('user', __name__)

dbsession = DBSession()

@user_bp.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['userpassword']
        
        # Query the database to check if the user exists
        dbsession = DBSession()
        user = dbsession.query(Employee).filter(Employee.email == useremail, Employee.password == password).first()
        dbsession.close()

        if user:
            session['username'] = user.name
            session['empid'] = user.empid
            return render_template('user/dashboard.html', username=session['username'])
        else:
            return render_template('index.html', message="Invalid username or password")
        
    if 'username' in session:
        return render_template('user/dashboard.html')
    else:
        return render_template('index.html' , message="You are not LoggedIn")

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')
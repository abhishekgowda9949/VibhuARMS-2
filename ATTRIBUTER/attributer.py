from flask import Blueprint, render_template, request,session
attributer_bp = Blueprint('attributer', __name__)
from database import DBSession,ATTRIBUTE_CO

@attributer_bp.route('/attributer_dashboard', methods=['GET', 'POST'])
def attributer_dashboard():
    if 'username' in session:
        return render_template('attributer/dashboard.html')
    
    if request.method == 'POST':
        attributeremail = request.form['attributeremail']
        attributerpassword = request.form['attributerpassword']
        
        # Query the database to check if the user exists
        dbsession = DBSession()
        attributer = dbsession.query(ATTRIBUTE_CO).filter(ATTRIBUTE_CO.emailid == attributeremail, ATTRIBUTE_CO.password == attributerpassword).first()
        dbsession.close()
        
        if attributer:
            session['username'] = attributer.name
            session['email'] = attributer.emailid
            return render_template('attributer/dashboard.html', username=session['username'])
        else:
            return render_template('index.html', message="Invalid username or Password")
    return render_template('index.html' , message="You are not LoggedIn")

@attributer_bp.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')
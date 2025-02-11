from flask import Blueprint, render_template, request,session
iqac_bp = Blueprint('iqac', __name__)
from database import IQAC_C0, DBSession, Metric_Details

@iqac_bp.route('/iqac_dashboard', methods=['GET', 'POST'])
def iqac_dashboard():
    if request.method == 'POST':
        iqacemail = request.form['iqacemail']
        password = request.form['iqacpassword']
        
        # Query the database to check if the user exists and fetching status
        dbsession = DBSession()
        user = dbsession.query(IQAC_C0).filter(IQAC_C0.emailid == iqacemail, IQAC_C0.password == password).first()
        total_metric_count = dbsession.query(Metric_Details).count()
        metric_Submited_count = dbsession.query(Metric_Details).filter(Metric_Details.attribute_status == 'Submitted').count()
        metric_Assigned_count = dbsession.query(Metric_Details).filter(Metric_Details.attribute_status == 'Assigned').count()
        metric_Working_count = dbsession.query(Metric_Details).filter(Metric_Details.attribute_status == 'Working').count()
        if metric_Assigned_count == 0:
            metric_Assigned_percentage = 0
        else:
            metric_Assigned_percentage = round((metric_Assigned_count/total_metric_count)*100,2)
        if metric_Submited_count == 0:
            metric_Submited_percentage = 0
        else:
            metric_Submited_percentage = round((metric_Submited_count/total_metric_count)*100,2)
        if metric_Working_count == 0:
            metric_Working_percentage = 0
        else:
            metric_Working_percentage = round((metric_Working_count/total_metric_count)*100,2)
        dbsession.close()
        session['data'] = {
        "complete": metric_Submited_percentage,
        "assigned": metric_Assigned_percentage,
        "working": metric_Working_percentage,
        "total_metrics_count" : total_metric_count,
        "metric_Submited_count" : metric_Submited_count,
        "metric_Assigned_count" :metric_Assigned_count,
        "metric_Working_count" : metric_Working_count
        }
        
        if user:
            session['username'] = user.name
            return render_template('iqac/dashboard.html', username=session['username'], data = session['data'])
        else:
            return render_template('index.html', message="Invalid username or Password")
    
    if 'username' not in session:
        return render_template('index.html',message="You are not LoggedIn")
    else:        
        dbsession = DBSession()
        total_metric_count = dbsession.query(Metric_Details).count()
        metric_Submited_count = dbsession.query(Metric_Details).filter(Metric_Details.attribute_status == 'Submitted').count()
        metric_Assigned_count = dbsession.query(Metric_Details).filter(Metric_Details.attribute_status == 'Assigned').count()
        metric_Working_count = dbsession.query(Metric_Details).filter(Metric_Details.attribute_status == 'Working').count()
        if metric_Assigned_count == 0:
            metric_Assigned_percentage = 0
        else:
            metric_Assigned_percentage = round((metric_Assigned_count/total_metric_count)*100,2)
        if metric_Submited_count == 0:
            metric_Submited_percentage = 0
        else:
            metric_Submited_percentage = round((metric_Submited_count/total_metric_count)*100,2)
        if metric_Working_count == 0:
            metric_Working_percentage = 0
        else:
            metric_Working_percentage = round((metric_Working_count/total_metric_count)*100,2)
        dbsession.close()
        session['data'] = {
            "complete": metric_Submited_percentage,
            "assigned": metric_Assigned_percentage,
            "working": metric_Working_percentage,
            "total_metrics_count" : total_metric_count,
            "metric_Submited_count" : metric_Submited_count,
            "metric_Assigned_count" :metric_Assigned_count,
            "metric_Working_count" : metric_Working_count
            }
        return render_template('iqac/dashboard.html',data = session['data'])

@iqac_bp.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')
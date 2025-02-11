from flask import Blueprint, render_template, request,session
attributer_bp = Blueprint('attributer', __name__)
from database import DBSession,ATTRIBUTE_CO, Metric_Details

@attributer_bp.route('/attributer_dashboard', methods=['GET', 'POST'])
def attributer_dashboard():
    if request.method == 'POST':
        attributeremail = request.form['attributeremail']
        attributerpassword = request.form['attributerpassword']
        
        # Query the database to check if the user exists
        dbsession = DBSession()
        attributer = dbsession.query(ATTRIBUTE_CO).filter(ATTRIBUTE_CO.emailid == attributeremail, ATTRIBUTE_CO.password == attributerpassword).first()
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
        dbsession.close()
        
        if attributer:
            session['username'] = attributer.name
            session['email'] = attributer.emailid
            return render_template('attributer/dashboard.html', username=session['username'], data = session['data'])
        else:
            return render_template('index.html', message="Invalid username or Password")
        
    if 'username' in session:
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
        return render_template('attributer/dashboard.html', data = session['data'])
    else:
        return render_template('index.html' , message="You are not LoggedIn")

@attributer_bp.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')
from flask import Blueprint, render_template, request, redirect, url_for, session
from database import ATTRIBUTE_ALLOT, DBSession, Metric_Assign

attributer_monitor_metrics_bp = Blueprint('attributer_monitor_metrics', __name__)

@attributer_monitor_metrics_bp.route('/attributer_monitor_metrics')
def attributer_monitor_metrics():
    # Check if the user is logged in, if not redirect to login page
    if 'email' not in session:
        return redirect(url_for('login'))

    # Open a new database session
    dbsession = DBSession()
    
    attibuteemail=session['email'] #Fetch Attributer Email ID
    attibuter_alloted_details = dbsession.query(ATTRIBUTE_ALLOT).filter(ATTRIBUTE_ALLOT.emailid == attibuteemail).first() #Fetch Attributer Alloted Attribute details
    attibuter_alloted_id = attibuter_alloted_details.attributeid #Fetch Attributer Alloted Attribute ID
    assigned_metrics = dbsession.query(Metric_Assign).filter(Metric_Assign.attribute_no == attibuter_alloted_id).all() # Fetch all assigned metrics
    
    # Close the database session
    dbsession.close()

    # Render the template with the fetched assigned metrics
    return render_template('attributer/attributer_monitor_metrics.html', assigned_metrics=assigned_metrics)
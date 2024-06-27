from flask import Blueprint, current_app, render_template, request, redirect, send_from_directory, url_for, session
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

@attributer_monitor_metrics_bp.route('/download/<string:file_id>/<path:filename>')
def download(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = metric_details.metric_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return "File not found.", 404
    
@attributer_monitor_metrics_bp.route('/view/<string:file_id>/<path:filename>')
def view(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = metric_details.metric_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found.", 404
    
import os

@attributer_monitor_metrics_bp.route('/delete/<string:file_id>/<filename>')
def delete(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == file_id).first()
    filenames = metric_details.metric_pdf.split(',')
    
    if filename in filenames:
        # Delete the file from disk
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove the filename from the database
        filenames.remove(filename)
        metric_details.metric_pdf = ','.join(filenames)
        
        dbsession.commit()
        
        return render_template('attributer/dashboard.html',message='PDF deleted successfully')
    else:
        return "File not found.", 404
from flask import Blueprint, current_app, render_template, request, redirect, send_from_directory, url_for, session
from database import DBSession, Metric_Details

iqac_monitor_attribute_bp = Blueprint('iqac_monitor_attribute', __name__)

@iqac_monitor_attribute_bp.route('/iqac_monitor_attribute')
def iqac_monitor_attribute():
    # Check if the user is logged in, if not redirect to login page
    if 'username' not in session:
        # Redirect to login page if user is not logged in
        return render_template('index.html', message="You are not logged in")

    # Open a new database session
    dbsession = DBSession()
    assigned_metrics = dbsession.query(Metric_Details).all() # Fetch all assigned metrics
    
    # Close the database session
    dbsession.close()

    # Render the template with the fetched assigned metrics
    return render_template('iqac/iqac_monitor_attribute.html', assigned_metrics=assigned_metrics)

@iqac_monitor_attribute_bp.route('/iqac_monitor_attribute_download/<string:file_id>/<path:filename>')
def iqac_monitor_attribute_download(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Details).filter(Metric_Details.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = metric_details.attribute_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return "File not found.", 404
    
@iqac_monitor_attribute_bp.route('/iqac_monitor_attribute_view/<string:file_id>/<path:filename>')
def iqac_monitor_attribute_view(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Details).filter(Metric_Details.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = metric_details.attribute_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found.", 404
    
import os

@iqac_monitor_attribute_bp.route('/iqac_monitor_attribute_delete/<string:file_id>/<filename>')
def iqac_monitor_attribute_delete(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Details).filter(Metric_Details.id == file_id).first()
    filenames = metric_details.attribute_pdf.split(',')
    
    if filename in filenames:
        # Delete the file from disk
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove the filename from the database
        filenames.remove(filename)
        metric_details.metric_pdf = ','.join(filenames)
        
        dbsession.commit()
        
        return render_template('iqac/dashboard.html',message='PDF deleted successfully')
    else:
        return "File not found.", 404
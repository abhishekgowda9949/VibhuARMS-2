import datetime
import os
from flask import Blueprint, current_app, flash, render_template, send_from_directory, session, redirect, url_for, jsonify, request
from database import ATTRIBUTE_ALLOT, DBSession, Employee, Metric_Assign, Metric_Details
from werkzeug.utils import secure_filename

attributer_metrics_remarks_bp = Blueprint('attributer_metrics_remarks', __name__)

@attributer_metrics_remarks_bp.route('/fetch_metric_details_remarks/<string:metric_id>')
def fetch_metric_details_remarks(metric_id):

    # Open a new database session
    dbsession = DBSession()
    try:
        # Fetch the metric details by metric ID
        metric = dbsession.query(Metric_Assign).filter(Metric_Assign.id == metric_id).first()
        if not metric:
            return jsonify({'error': 'Metric not found'}), 404
        
    finally:
        # Close the database session
        dbsession.close()

    # Render the template with metric and employee details
    return render_template(
        'attributer/attributer_remarks.html', 
        metric=metric
    )

@attributer_metrics_remarks_bp.route('/submit_remarks', methods=['POST'])
def submit_remarks():
    # Get form data
    metric_id = request.form.get('metric_id')
    attribute_no = request.form.get('attribute_no')
    metric_no = request.form.get('metric_no')
    metric_remarks = request.form.get('metric_remarks')

    # Open a new database session
    dbsession = DBSession()
    metric = dbsession.query(Metric_Assign).filter(Metric_Assign.id == metric_id, Metric_Assign.attribute_no == attribute_no, Metric_Assign.metric_no == metric_no).first()
    if metric:
        metric.metric_remarks = metric_remarks
        dbsession.commit()

    # Close the database session
    dbsession.close()

    return render_template('attributer/dashboard.html' , message ="Your Metric Remarks are Sucessfull Updated")
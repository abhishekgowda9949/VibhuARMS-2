import calendar
from datetime import datetime
import json
from flask import Blueprint, current_app, jsonify, render_template, request, send_from_directory, session
from database import DBSession, Metric_Assign , Employee

user_view_metrics_bp = Blueprint('user_view_metrics', __name__)

@user_view_metrics_bp.route('/user_view_metrics')
def user_view_metrics():    
    # Check if user is logged in
    if 'username' in session:
        username = session['username']
        empid = session['empid']
        dbsession = DBSession()
        metrics = dbsession.query(Metric_Assign).filter(Metric_Assign.employee_id == empid)
        dbsession.close()  # Remember to close the session
        current_month = datetime.now().strftime('%B %Y')
        return render_template('user/user_view_metrics.html', metrics=metrics, current_month = current_month)
    else:
        # Redirect to login page if user is not logged in
        return render_template('user/login.html', message="You are not LoggedIn")
    
@user_view_metrics_bp.route('/metric_file_view/<string:metricid>/<path:filename>')
def metric_file_view(metricid, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == metricid).first()
    dbsession.close()  # Remember to close the session
    filenames = metric_details.metric_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found.", 404
    
@user_view_metrics_bp.route('/metric_file_download/<string:metricid>/<path:filename>')
def metric_file_download(metricid, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == metricid).first()
    filenames = metric_details.metric_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return "File not found.", 404

@user_view_metrics_bp.route('/user_update_details', methods=['POST'])
def user_update_details():

    MetricId = request.form.get('metric_id')
    if not MetricId:
        return jsonify({'error': 'Metric ID is required'}), 400
    # Assuming DBSession and Target model are defined correctly
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == MetricId).first()
    if metric_details:
        empid = session['empid']
        employee_details = dbsession.query(Employee).filter(Employee.empid == empid).first()
        employee_name = employee_details.name
        return render_template("user/user_update_metric.html", metric_details=metric_details, employee_name = employee_name)
    else:
        return jsonify(message='Metric Details not found'), 404
    
# @user_view_targets_bp.route('/raise_ticket/<parameter_id>')
# def raise_ticket(parameter_id):
#     dbsession = DBSession()
#     target_details = dbsession.query(Target).filter_by(parameter_id=parameter_id).first()
#     return render_template("user/raise_ticket.html",target_details=target_details)
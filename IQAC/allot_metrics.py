import datetime
import os
from flask import Blueprint, current_app, flash, render_template, send_from_directory, session, redirect, url_for, jsonify, request
from database import DBSession, Employee, Metric_Assign, Metric_Details
from werkzeug.utils import secure_filename

allot_metrics_bp = Blueprint('allot_metrics', __name__)

@allot_metrics_bp.route('/allot_metrics')
def allot_metrics():

    # Open a new database session
    dbsession = DBSession()
    try:
        # Fetch metrics corresponding to the attribute IDs
        metrics = dbsession.query(Metric_Details).all()
    finally:
        # Close the database session
        dbsession.close()

    # Render the template with the fetched metrics
    return render_template('iqac/allot_metrics.html', metrics=metrics)

@allot_metrics_bp.route('/fetch_metric_details', methods=['POST'])
def fetch_metric_details():
    # Get the metric ID from the POST request
    metric_id = request.form.get('metric_id')
    if not metric_id:
        return jsonify({'error': 'Metric ID is required'}), 400

    # Open a new database session
    dbsession = DBSession()
    try:
        # Fetch the metric details by metric ID
        metric = dbsession.query(Metric_Details).filter(Metric_Details.metric_no == metric_id).first()
        if not metric:
            return jsonify({'error': 'Metric not found'}), 404

        # Fetch all employees (you may want to filter based on requirements)
        employees = dbsession.query(Employee).all()
    finally:
        # Close the database session
        dbsession.close()

    # Prepare metric details for the template
    metric_details = {
        'attribute_no': metric.attribute_no,
        'metric_no': metric.metric_no,
        'metric_description': metric.metric_description,
        'documents_required': metric.documents_required,
        'weightage': metric.weightage
    }

    # Prepare a list of employee details for the template
    employee_details_list = []
    for employee in employees:
        employee_details_list.append({
            'id': employee.id,
            'name': employee.name,
            'empid': employee.empid,
            'department': employee.department,
            'email': employee.email,
            'mobile': employee.mobile
        })

    # Render the template with metric and employee details
    return render_template(
        'iqac/allot_metrics_2.html', 
        metric=metric_details,
        employees=employee_details_list
    )

@allot_metrics_bp.route('/submit_metric', methods=['POST'])
def submit_metric():
    # Get form data
    attribute_no = request.form.get('attribute_no')
    metric_no = request.form.get('metric_no')
    metric_description = request.form.get('metric_description')
    calendar_type = request.form.get('calendar_type')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    weightage = request.form.get('weightage')
    department = request.form.get('department')
    program = request.form.get('program')
    employee_id = request.form.get('employee_id')
    alloted_targets = request.form.get('alloted_target')

    # Open a new database session
    dbsession = DBSession()

    metric_assigned_details = dbsession.query(Metric_Assign).filter(Metric_Assign.metric_no == metric_no, Metric_Assign.department == department, Metric_Assign.program == program, Metric_Assign.employee_id == employee_id).first()
    if metric_assigned_details:
        return render_template('iqac/dashboard.html' , message ="Your Metric Already Assigned to Same User")
    else:
    # Create a new Metric_Assign instance
        new_metric_assign = Metric_Assign(
            attribute_no=attribute_no,
            metric_no=metric_no,
            metric_description=metric_description,
            calendar_type = calendar_type,
            start_date=start_date,
            end_date=end_date,
            weightage=weightage,
            department=department,
            program=program,
            employee_id=employee_id,
            alotted_target_no = alloted_targets,
            metric_status = 'Assigned'
        )

        # Add to the session and commit
        dbsession.add(new_metric_assign)
        metric_details = dbsession.query(Metric_Details).filter(Metric_Details.metric_no == metric_no).first()
        metric_details.attribute_status = 'Assigned'
        dbsession.commit()

        # Provide feedback to the user
        flash('Metric assigned successfully!', 'success')

        # Close the database session
        dbsession.close()

        return render_template('iqac/dashboard.html' , message ="Your Metric Assignment Sucessfull")
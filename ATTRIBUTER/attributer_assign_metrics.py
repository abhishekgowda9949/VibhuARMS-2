from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from database import ATTRIBUTE_ALLOT, DBSession, Employee, Metric_Details

attributer_assign_metrics_bp = Blueprint('attributer_assign_metrics', __name__)

@attributer_assign_metrics_bp.route('/attributer_assign_metrics')
def attributer_assign_metrics():
    # Check if the user is logged in, if not redirect to login page
    if 'email' not in session:
        return redirect(url_for('login'))

    # Open a new database session
    dbsession = DBSession()
    try:
        # Get the email ID from the session
        attributer_emailid = session['email']
        # Fetch attribute allocations for the logged-in user
        attributer_alloc = dbsession.query(ATTRIBUTE_ALLOT).filter(ATTRIBUTE_ALLOT.emailid == attributer_emailid).all()
        
        # Collect all attribute IDs from the fetched allocations
        attributer_alloc_ids = [alloc.attributeid for alloc in attributer_alloc]

        # Fetch metrics corresponding to the attribute IDs
        metrics = dbsession.query(Metric_Details).filter(Metric_Details.attribute_no.in_(attributer_alloc_ids)).all()
    finally:
        # Close the database session
        dbsession.close()

    # Render the template with the fetched metrics
    return render_template('attributer/attributer_assign_metrics.html', metrics=metrics)

@attributer_assign_metrics_bp.route('/fetch_metric_details', methods=['POST'])
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
        'attributer/attributer_assign_metrics_2.html', 
        metric=metric_details,
        employees=employee_details_list
    )

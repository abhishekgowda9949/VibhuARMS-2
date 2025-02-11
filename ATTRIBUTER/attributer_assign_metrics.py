import datetime
import os
from flask import Blueprint, current_app, flash, render_template, send_from_directory, session, redirect, url_for, jsonify, request
from database import ATTRIBUTE_ALLOT, DBSession, Employee, Metric_Assign, Metric_Details
from werkzeug.utils import secure_filename

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

@attributer_assign_metrics_bp.route('/submit_metric', methods=['POST'])
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
        return render_template('attributer/dashboard.html' , message ="Your Metric Already Assigned to Same User")
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

        return render_template('attributer/dashboard.html' , message ="Your Metric Assignment Sucessfull")

@attributer_assign_metrics_bp.route('/upload_pdf', methods=['POST'])
def upload_pdf():
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
    finally:
        # Close the database session
        dbsession.close()

    # Prepare metric details for the template
    metric_details = {
        'id':metric.id,
        'attribute_no': metric.attribute_no,
        'metric_no': metric.metric_no,
        'metric_description': metric.metric_description,
        'documents_required': metric.documents_required,
        'weightage': metric.weightage
    }

    # Render the template with metric and employee details
    return render_template(
        'attributer/attributer_upload_pdf.html', 
        metric=metric_details
    )

@attributer_assign_metrics_bp.route('/submit_documents', methods=['GET', 'POST'])
def submit_documents():
    if 'username' not in session:
        # Redirect to login page if user is not logged in
        return render_template('index.html', message="You are not logged in")

    metric_detail_id = request.form['metric_detail_id']

    username = session['username']
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Details).filter(Metric_Details.id == metric_detail_id).first()

    if metric_details:            
        uploaded_files = request.files.getlist('attribute_files[]')
        if uploaded_files and uploaded_files[0].filename != '':
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Process each uploaded file
            new_filenames = []
            for file in uploaded_files:
                # Append current datetime to the filename
                filename = current_datetime + '_' + secure_filename(file.filename)
                new_filenames.append(filename)
        
                # Save the file to disk
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                
            if metric_details.attribute_pdf is None:
                metric_details.attribute_pdf = new_filenames
                updated_filenames = ','.join(new_filenames)  # Initialize updated_filenames for new record
            else:
                existing_filenames = metric_details.attribute_pdf if metric_details.attribute_pdf else ""
                updated_filenames = ','.join([existing_filenames, *new_filenames]) if existing_filenames else ','.join(new_filenames)
                metric_details.attribute_pdf = updated_filenames

        metric_details.attribute_status = request.form['attribute_status']
        dbsession.commit()
        dbsession.close()
            
        return render_template('attributer/dashboard.html', message ="Documents Upload Sucessfull")
    
@attributer_assign_metrics_bp.route('/attributer_file_download/<string:file_id>/<path:filename>')
def attributer_file_download(file_id, filename):
    dbsession = DBSession()
    targets = dbsession.query(Metric_Details).filter(Metric_Details.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = targets.attribute_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return "File not found.", 404
    
@attributer_assign_metrics_bp.route('/attributer_file_view/<string:file_id>/<path:filename>')
def attributer_file_view(file_id, filename):
    dbsession = DBSession()
    pdftarget = dbsession.query(Metric_Details).filter(Metric_Details.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = pdftarget.attribute_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found.", 404
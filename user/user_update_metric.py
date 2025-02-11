import calendar
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify ,current_app
from database import DBSession, Metric_Assign
from werkzeug.utils import secure_filename
import datetime

user_update_metric_bp = Blueprint('user_update_metric', __name__)



@user_update_metric_bp.route('/user_update_metric', methods=['GET', 'POST'])
def user_update_metric():
    if 'username' not in session:
        # Redirect to login page if user is not logged in
        return render_template('index.html', message="You are not logged in")

    metric_assign_id = request.form['metric_assign_id']

    username = session['username']
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == metric_assign_id).first()

    if metric_details:            
        uploaded_files = request.files.getlist('files[]')
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
                
            if metric_details.metric_pdf is None:
                metric_details.metric_pdf = new_filenames
                updated_filenames = ','.join(new_filenames)  # Initialize updated_filenames for new record
            else:
                existing_filenames = metric_details.metric_pdf if metric_details.metric_pdf else ""
                updated_filenames = ','.join([existing_filenames, *new_filenames]) if existing_filenames else ','.join(new_filenames)
                metric_details.metric_pdf = updated_filenames
                
        metric_details.metric_status = request.form['metric_status']
        metric_details.completed_target_no =request.form['completed_target']
        dbsession.commit()
        dbsession.close()
            
        return render_template('user/dashboard.html', messages ="Update Metric Sucessfull")
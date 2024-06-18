import calendar
from datetime import datetime
from flask import Blueprint, current_app, jsonify, render_template, request, send_from_directory, session
from database import DBSession, Responsibility, Target

view_targets_bp = Blueprint('view_targets', __name__)

@view_targets_bp.route('/view_targets')
def view_targets():
    
    # Check if user is logged in
    if 'username' in session:
        username = session['username']
        dbsession = DBSession()
        targets = dbsession.query(Target).all()
        dbsession.close()  # Remember to close the session
        current_month = datetime.now().strftime('%B %Y')
        return render_template('admin/view_targets.html', targets=targets, current_month = current_month)
    else:
        # Redirect to login page if user is not logged in
        return render_template('admin/login.html', message="You are not LoggedIn")
    
@view_targets_bp.route('/download/<string:file_id>/<path:filename>')
def download(file_id, filename):
    dbsession = DBSession()
    targets = dbsession.query(Target).filter(Target.parameter_id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = targets.target_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return "File not found.", 404
    
@view_targets_bp.route('/view/<string:file_id>/<path:filename>')
def view(file_id, filename):
    dbsession = DBSession()
    pdftarget = dbsession.query(Target).filter(Target.parameter_id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = pdftarget.target_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found.", 404
    
import os

@view_targets_bp.route('/delete/<string:file_id>/<filename>')
def delete(file_id, filename):
    dbsession = DBSession()
    file = dbsession.query(Target).filter(Target.parameter_id == file_id).first()
    filenames = file.target_pdf.split(',')
    
    if filename in filenames:
        # Delete the file from disk
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove the filename from the database
        filenames.remove(filename)
        file.target_pdf = ','.join(filenames)
        
        dbsession.commit()
        
        return render_template('admin/dashboard.html',message='PDF deleted successfully')
    else:
        return "File not found.", 404

@view_targets_bp.route('/edit_page/<parameter_id>')
def edit_page(parameter_id):
    try:
        # Assuming DBSession and Target model are defined correctly
        dbsession = DBSession()
        target_details = dbsession.query(Target).filter_by(parameter_id=parameter_id).first()
        if target_details:
            start_month = target_details.startingmonth
            end_month = target_details.endingmonth

            months = generate_month_list(start_month, end_month)
            session['months'] = months

            responsibilities = dbsession.query(Responsibility).all()
            responsibility_names = [responsibility.name for responsibility in responsibilities]
            
            # Assuming set_target_part2.html exists and contains the necessary data for rendering
            return render_template("admin/set_target_part2.html", months=months, responsibility_names=responsibility_names, target_details=target_details)
        else:
            return jsonify(message='Target details not found'), 404
    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {str(e)}")
        # Return an error response
        return jsonify(message='An error occurred'), 500
    
@view_targets_bp.route('/delete_page/<parameter_id>')
def delete_page(parameter_id):
    try:
        # Obtain a session object
        dbsession = DBSession()

        # Query the record to be deleted
        target_details = dbsession.query(Target).filter_by(parameter_id=parameter_id).first()

        # If the record exists, delete it
        if target_details:
            dbsession.delete(target_details)
            dbsession.commit()
            return render_template('admin/dashboard.html',message='Item deleted successfully'), 200
        else:
            return jsonify(message='Item not found'), 404
    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {str(e)}")
        return jsonify(message='Failed to delete item'), 500
    
def generate_month_list(start_month, end_month):
    # Parse the starting and ending months
    start_year, start_month = map(int, start_month.split('-'))
    end_year, end_month = map(int, end_month.split('-'))
    
    # Generate a list of months between the start and end months
    month_list = []
    while (start_year, start_month) <= (end_year, end_month):
        month_name = calendar.month_name[start_month]
        month_list.append(f"{month_name} {start_year}")
        start_month += 1
        if start_month > 12:
            start_month = 1
            start_year += 1
    
    return month_list
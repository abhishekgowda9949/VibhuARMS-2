import calendar
from datetime import datetime
import json
from flask import Blueprint, current_app, jsonify, render_template, send_from_directory, session
from database import DBSession, Metric_Assign

user_view_targets_bp = Blueprint('user_view_targets', __name__)

@user_view_targets_bp.route('/user_view_targets')
def user_view_targets():    
    # Check if user is logged in
    if 'username' in session:
        username = session['username']
        empid = session['empid']
        dbsession = DBSession()
        targets = dbsession.query(Metric_Assign).filter(Metric_Assign.employee_id == empid)
        dbsession.close()  # Remember to close the session
        current_month = datetime.now().strftime('%B %Y')
        return render_template('user/user_view_targets.html', targets=targets, current_month = current_month)
    else:
        # Redirect to login page if user is not logged in
        return render_template('user/login.html', message="You are not LoggedIn")
    
# @user_view_targets_bp.route('/download/<string:file_id>/<path:filename>')
# def download(file_id, filename):
#     dbsession = DBSession()
#     targets = dbsession.query(Target).filter(Target.parameter_id == file_id).first()
#     filenames = targets.target_pdf.split(',')
    
#     if filename in filenames:
#         return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
#     else:
#         return "File not found.", 404

# @user_view_targets_bp.route('/user_edit_page/<parameter_id>')
# def user_edit_page(parameter_id):
#     try:
#         # Assuming DBSession and Target model are defined correctly
#         dbsession = DBSession()
#         target_details = dbsession.query(Target).filter_by(parameter_id=parameter_id).first()
#         if target_details:
#             start_month = target_details.startingmonth
#             end_month = target_details.endingmonth

#             months = generate_month_list(start_month, end_month)
#             session['months'] = months

#             responsibilities = dbsession.query(Responsibility).all()
#             responsibility_names = [responsibility.name for responsibility in responsibilities]
            
#             # Assuming set_target_part2.html exists and contains the necessary data for rendering
#             return render_template("user/update_target.html", months=months, responsibility_names=responsibility_names, target_details=target_details)
#         else:
#             return jsonify(message='Target details not found'), 404
#     except Exception as e:
#         # Log the exception for debugging
#         print(f"An error occurred: {str(e)}")
#         # Return an error response
#         return jsonify(message='An error occurred'), 500
    
# @user_view_targets_bp.route('/raise_ticket/<parameter_id>')
# def raise_ticket(parameter_id):
#     dbsession = DBSession()
#     target_details = dbsession.query(Target).filter_by(parameter_id=parameter_id).first()
#     return render_template("user/raise_ticket.html",target_details=target_details)
    
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
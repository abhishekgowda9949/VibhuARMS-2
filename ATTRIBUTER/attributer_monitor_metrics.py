from flask import Blueprint, current_app, render_template, request, redirect, send_from_directory, url_for, session
from database import ATTRIBUTE_ALLOT, DBSession, Employee, Metric_Assign

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
    if attibuter_alloted_details:
        attibuter_alloted_id = attibuter_alloted_details.attributeid #Fetch Attributer Alloted Attribute ID
        assigned_metrics = dbsession.query(Metric_Assign).filter(Metric_Assign.attribute_no == attibuter_alloted_id).all() # Fetch all assigned metrics
        
    # Render the template with the fetched assigned metrics
        return render_template('attributer/attributer_monitor_metrics.html', assigned_metrics=assigned_metrics)
    # Close the database session
    dbsession.close()

    # Render the template with the fetched assigned metrics
    return render_template('attributer/attributer_monitor_metrics.html')

@attributer_monitor_metrics_bp.route('/monitor_metric_download/<string:file_id>/<path:filename>')
def monitor_metric_download(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = metric_details.metric_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return "File not found.", 404
    
@attributer_monitor_metrics_bp.route('/monitor_metric_view/<string:file_id>/<path:filename>')
def monitor_metric_view(file_id, filename):
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == file_id).first()
    dbsession.close()  # Remember to close the session
    filenames = metric_details.metric_pdf.split(',')
    
    if filename in filenames:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found.", 404
    
import os

@attributer_monitor_metrics_bp.route('/monitor_metric_delete/<string:file_id>/<filename>')
def monitor_metric_delete(file_id, filename):
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
    
@attributer_monitor_metrics_bp.route('/attributer_monitor_metric_mail/<string:file_id>')
def attributer_monitor_metric_mail(file_id):    
    dbsession = DBSession()
    metric_details = dbsession.query(Metric_Assign).filter(Metric_Assign.id == file_id).first()
    employee_details = dbsession.query(Employee).filter(Employee.empid == metric_details.employee_id).first()
    emailid = employee_details.email
    send_mail(metric_details, emailid)
    return render_template('attributer/dashboard.html',message='Mail Sent Sucessfuly')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(metric_details, emailid):
    # Construct the subject
    subject = f"Metric Status: {metric_details.metric_status}"

    # Construct the email body
    body = f"""
    Attribute No: {metric_details.attribute_no}
    Metric No: {metric_details.metric_no}
    Metric Description: {metric_details.metric_description}
    Calendar Type: {metric_details.calendar_type}
    Start Date: {metric_details.start_date}
    End Date: {metric_details.end_date}
    Weightage: {metric_details.weightage}
    Department: {metric_details.department}
    Program: {metric_details.program}
    Employee ID: {metric_details.employee_id}
    Metric PDF: {metric_details.metric_pdf}
    Metric Status: {metric_details.metric_status}
    Meric Remarks: {metric_details.metric_remarks}
    """

    # Sender and receiver details
    sender_email = "abhisektn@gmail.com"
    sender_password = "xrad sisd pztc lwvx"  # Be careful with storing passwords in code
    receiver_email = emailid

    # Create the email headers and set the sender and receiver email addresses
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message body to the email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS for security

        # Log in to the server using the provided credentials
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)

        # Disconnect from the server
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
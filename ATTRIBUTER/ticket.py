from email import message
import os
from flask import Blueprint, current_app, render_template, request, session

from database import DBSession, Responsibility, Target, Ticket

ticket_bp=Blueprint('ticket', __name__)

@ticket_bp.route('/view_ticket', methods=['GET', 'POST'])
def view_ticket():
    if 'username' not in session:
        # Redirect to login page if user is not logged in
        return render_template('admin/login.html', message="You are not logged in")
    
    dbsession = DBSession()
    tickets = dbsession.query(Ticket).filter(Ticket.ticket_status == 'Raised')
    dbsession.close()

    return render_template('admin/view_ticket.html',tickets=tickets)

@ticket_bp.route('/fetchdetails/<int:id>')
def fetchdetails(id):
    dbsession = DBSession()

    tickets = dbsession.query(Ticket).filter(Ticket.id == id).first()

    responsibilities = dbsession.query(Responsibility).all()
    responsibility_names = [responsibility.name for responsibility in responsibilities]

    dbsession.close()
    return render_template('admin/resolve_ticket.html',ticket_details=tickets,responsibility_names=responsibility_names)

@ticket_bp.route('/resolved_ticket', methods=['GET', 'POST'])
def resolved_ticket():
    if request.method == 'POST':
        parameter_id = request.form['parameterid']
        ticket_id = request.form['ticketid']
        parameter_name = request.form['parametername']
        parameter_description = request.form['parameterdescription']
        ticket_description = request.form['ticketdescription']
        responsibility = request.form['responsibility']

        session = DBSession()

        try:
            target = session.query(Target).filter(Target.parameter_id == parameter_id).first()
            
            if target:
                # Update the attributes of the object
                target.parameter_name = parameter_name
                target.parameter_description = parameter_description
                target.responsibility = responsibility
                delete(parameter_id, ticket_description)  # Ensure this function is defined and works properly
            
                ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
                if ticket:
                    ticket.ticket_status = 'Solved'

            session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

        return render_template('admin/dashboard.html', message="Changes Successfully Completed")
    
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
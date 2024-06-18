import calendar
from flask import Blueprint, render_template, request,session
from database import DBSession, Responsibility, Target

# Get a session
dbsession = DBSession()

set_target_bp = Blueprint('set_target', __name__)

@set_target_bp.route('/set_target')
def set_target():
    # Check if user is logged in
    if 'username' in session:
        username = session['username']
        return render_template("admin/set_target_part1.html", username=username)
    else:
        # Redirect to login page if user is not logged in
        return render_template('admin/login.html', message="You are not LoggedIn")

@set_target_bp.route('/submit_target', methods=['POST'])
def submit_target():
    if request.method == 'POST':
        target_type = request.form['targetType']

        calendar = request.form['calendar']
        department = request.form['department']
        program = request.form['program']
        parameter_id = request.form['parameterid']
        parameter_name = request.form['parametername']
        parameter_description = request.form['parameterdescription']
        responsibility = request.form['responsibility']

        dbsession = DBSession()
        target = dbsession.query(Target).filter(Target.calendartype == calendar, Target.department == department, Target.program == program, Target.parameter_id == parameter_id).first()
        email = dbsession.query(Responsibility).filter(Responsibility.name == responsibility ).first()
        emailid = email.emailid

        if target_type == 'monthly':
            months = session['months']
            monthly_targets = {}
            completed_monthly_targets = {}
            for month in months:
                target_name = 'target_' + month.lower()
                target_value = request.form[target_name]
                monthly_targets[month] = target_value
                if target.completed_target_details is None:
                    completed_target_value = '0'
                    completed_monthly_targets[month] = completed_target_value
                else:
                    completed_monthly_targets = target.completed_target_details

        elif target_type == 'yearly':
            completed_monthly_targets = '0'
            number_of_target = request.form['numberOfTargets']

        if target:
            # Update the attributes of the object
            target.parameter_name = parameter_name
            target.parameter_description = parameter_description
            target.responsibility = responsibility
            target.target_type = target_type
            target.emailid = emailid
            if target_type == 'monthly':
                target.target_details = monthly_targets  # Assuming target_details is a relationship or a JSON column
            elif target_type == 'yearly':
                target.target_details = number_of_target 
            target.completed_target_details = completed_monthly_targets # Assuming completed_target_details is a relationship or a JSON column
            target.target_status = "Alotted"

            # Commit the changes to the database
            dbsession.commit()
            
            target_details = dbsession.query(Target).filter(Target.parameter_id == parameter_id).first()

            return render_template("admin/dashboard.html", message="Set Target Details Successfully Saved",targets=target_details)

        else:
            return render_template("admin/dashboard.html", message="Target not found")

@set_target_bp.route('/load_target', methods=['POST'])
def load_target():
    parameter_id = request.form['parameterid']
    dbsession = DBSession()
    target_details = dbsession.query(Target).filter_by(parameter_id=parameter_id).first()
    if target_details:
        start_month = target_details.startingmonth
        end_month = target_details.endingmonth

        months = generate_month_list(start_month, end_month)
        session['months'] = months

        responsibilities = dbsession.query(Responsibility).all()
        responsibility_names = [responsibility.name for responsibility in responsibilities]

        return render_template("admin/set_target_part2.html",months=months,responsibility_names=responsibility_names,target_details=target_details)
    
    else:
        return render_template("admin/set_target_part1.html", message = "Details not Found For Parameter ID Provided")


@set_target_bp.route('/set_target_part1', methods=['POST'])
def set_target_part1():
    parameter_id = request.form['parameterid']
    calendar_select = request.form['calendarSelect']
    start_Month = request.form['startMonth']
    end_Month = request.form['endMonth']
    department_select = request.form['departmentSelect']
    program_select = request.form['programSelect']

    months = generate_month_list(start_Month, end_Month)
    session['months'] = months

    set_target_details(calendar_select,start_Month,end_Month,department_select,program_select,parameter_id)
    
    dbsession=DBSession()
    responsibilities = dbsession.query(Responsibility).all()
    responsibility_names = [responsibility.name for responsibility in responsibilities]
    
    target_details = dbsession.query(Target).filter_by(parameter_id=parameter_id).first()
    
    return render_template("admin/set_target_part2.html",months=months,responsibility_names=responsibility_names,target_details=target_details)

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

# Insert a name into the database
def set_target_details(calendar_select,start_Month,end_Month,department_select,program_select,parameter_id):
    set_new_calender = Target(calendartype=calendar_select,startingmonth=start_Month,endingmonth=end_Month,department=department_select,program=program_select,parameter_id=parameter_id)
    dbsession.add(set_new_calender)
    dbsession.commit()
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
from database import Employee, DBSession  # Adjust import for Employee model

import_employee_bp = Blueprint('import_employee', __name__)

@import_employee_bp.route('/import_employee', methods=['GET', 'POST'])
def import_employee():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            
            try:
                df = pd.read_excel(file_path)
                
                dbsession = DBSession()
                
                for index, row in df.iterrows():
                    new_employee = Employee(
                        empid=row['empid'],
                        name=row['name'],
                        department=row['department'],
                        email=row['email'],
                        mobile=row['Mobile'],  # Adjust column name based on your Excel file
                        password=row['password']
                    )
                    
                    dbsession.add(new_employee)
                
                dbsession.commit()
                
            except Exception as e:
                flash(f'Error importing employees: {str(e)}', 'error')
                dbsession.rollback()
                
            finally:
                dbsession.close()
                os.remove(file_path)  # Remove the uploaded file after processing
                
            return render_template('iqac/dashboard.html' , messages ="Employees Successfully Imported")
    
    return render_template('iqac/import_employee.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xls', 'xlsx'}

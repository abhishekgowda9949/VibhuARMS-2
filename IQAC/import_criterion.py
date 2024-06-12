import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
from database import CRITERIA_CO, DBSession

import_criteria_bp = Blueprint('import_criteria', __name__)

@import_criteria_bp.route('/import_criteria', methods=['GET', 'POST'])
def import_criteria():
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
            
            df = pd.read_excel(file_path)
            
            dbsession = DBSession()
            
            for index, row in df.iterrows():
                new_criterion = CRITERIA_CO(
                    name=row['name'],
                    emailid=row['emailid'],
                    password=row['password']
                )
                
                dbsession.add(new_criterion)
            
            dbsession.commit()
            dbsession.close()
            
            return render_template('iqac/dashboard.html' , messages ="CriteriOn Users Successfully Imported")
    
    return render_template('iqac/import_criterion.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xls', 'xlsx'}

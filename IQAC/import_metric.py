import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
from database import DBSession, Metric_Details # Ensure Metric model is correctly imported
import numpy as np

import_metric_bp = Blueprint('import_metric', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@import_metric_bp.route('/import_metric', methods=['GET', 'POST'])
def import_metric():
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
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            try:
                df = pd.read_excel(file_path)
                df = df.replace({np.nan: None})  # Replace nan with None
                
                dbsession = DBSession()
                
                for index, row in df.iterrows():
                    new_metric = Metric_Details(
                        attribute_no=row['attribute_no'],
                        metric_no=row['metric_no'],
                        metric_description=row['metric_description'],
                        documents_required=row['documents_required'],
                        weightage=row['weightage']
                    )
                    
                    dbsession.add(new_metric)
                
                dbsession.commit()
                
            except Exception as e:
                flash(f'Error importing metrics: {str(e)}', 'error')
                dbsession.rollback()
                
            finally:
                dbsession.close()
                os.remove(file_path)  # Remove the uploaded file after processing
                
            return render_template('iqac/dashboard.html', messages="Metrics Successfully Imported")
    
    return render_template('iqac/import_metric.html')

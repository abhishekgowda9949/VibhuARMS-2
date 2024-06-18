import os
from flask import Flask, render_template
from database import DBSession

#IQAC
from IQAC.iqac import iqac_bp
from IQAC.iqac_change_password import iqac_change_password_bp
from IQAC.allot_attributer import allot_attributer_bp
from IQAC.import_attributer import import_attributer_bp
from IQAC.import_employee import import_employee_bp
from IQAC.import_metric import import_metric_bp

#ATTRIBUTER
from ATTRIBUTER.attributer import attributer_bp
from ATTRIBUTER.attributer_change_password import attributer_change_password_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dbsession = DBSession()

#IQAC
app.register_blueprint(iqac_bp)
app.register_blueprint(iqac_change_password_bp)
app.register_blueprint(allot_attributer_bp)
app.register_blueprint(import_attributer_bp)
app.register_blueprint(import_employee_bp)
app.register_blueprint(import_metric_bp)

#ATTRIBUTER
app.register_blueprint(attributer_bp)
app.register_blueprint(attributer_change_password_bp)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
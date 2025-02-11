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
from IQAC.import_provision import import_provision_bp
from IQAC.iqac_monitor_metric import iqac_monitor_metrics_bp
from IQAC.iqac_monitor_attribute import iqac_monitor_attribute_bp
from IQAC.allot_metrics import allot_metrics_bp

#ATTRIBUTER
from ATTRIBUTER.attributer import attributer_bp
from ATTRIBUTER.attributer_change_password import attributer_change_password_bp
from ATTRIBUTER.attributer_assign_metrics import attributer_assign_metrics_bp
from ATTRIBUTER.attributer_monitor_metrics import attributer_monitor_metrics_bp
from ATTRIBUTER.attributer_metrics_remarks import attributer_metrics_remarks_bp

#USER
from user.user import user_bp
from user.user_change_password import user_change_password_bp
from user.user_view_metrics import user_view_metrics_bp
from user.user_update_metric import user_update_metric_bp

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
app.register_blueprint(import_provision_bp)
app.register_blueprint(iqac_monitor_metrics_bp)
app.register_blueprint(iqac_monitor_attribute_bp)
app.register_blueprint(allot_metrics_bp)

#ATTRIBUTER
app.register_blueprint(attributer_bp)
app.register_blueprint(attributer_change_password_bp)
app.register_blueprint(attributer_assign_metrics_bp)
app.register_blueprint(attributer_monitor_metrics_bp)
app.register_blueprint(attributer_metrics_remarks_bp)

#USER
app.register_blueprint(user_bp)
app.register_blueprint(user_change_password_bp)
app.register_blueprint(user_view_metrics_bp)
app.register_blueprint(user_update_metric_bp)

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
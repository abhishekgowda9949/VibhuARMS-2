import os
from flask import Flask, render_template
from database import DBSession

#IQAC
from IQAC.iqac import iqac_bp
from IQAC.iqac_change_password import iqac_change_password_bp
from IQAC.allot_criterion import allot_criterion_bp

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
app.register_blueprint(allot_criterion_bp)

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
from flask import Blueprint, render_template, request, session
allot_criterion_bp = Blueprint('allot_criterion', __name__)
from database import CRITERIA_CO, DBSession

@allot_criterion_bp.route('/allot_criterion')
def allot_criterion():
    # Fetch Criterion names from the database
    dbsession = DBSession()
    Criterion_Details = dbsession.query(CRITERIA_CO.name).all()
    dbsession.close()
    
    # Pass the Criterion Names to the template
    return render_template('iqac/allot_criterion.html', Criterion_Details=Criterion_Details)
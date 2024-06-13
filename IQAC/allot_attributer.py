from flask import Blueprint, render_template, request, session
allot_attributer_bp = Blueprint('allot_attributer', __name__)
from database import ATTRIBUTE_CO, DBSession

@allot_attributer_bp.route('/allot_attributer')
def allot_attributer():
    # Fetch Criterion names from the database
    dbsession = DBSession()
    Attributer_Details = dbsession.query(ATTRIBUTE_CO.name).all()
    dbsession.close()
    
    # Pass the Criterion Names to the template
    return render_template('iqac/allot_attributer.html', Attributer_Details=Attributer_Details)
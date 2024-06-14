from flask import Blueprint, jsonify, render_template, request
from database import ATTRIBUTE_CO, DBSession

allot_attributer_bp = Blueprint('allot_attributer', __name__)

@allot_attributer_bp.route('/allot_attributer')
def allot_attributer():
    with DBSession() as session:
        # Fetch Attributer names from the database
        Attributer_Details = session.query(ATTRIBUTE_CO.name).all()
    
    # Pass the Attributer Names to the template
    return render_template('iqac/allot_attributer.html', Attributer_Details=Attributer_Details)

@allot_attributer_bp.route('/get_attributer_details', methods=['POST'])
def get_attributer_details():
    data = request.get_json()
    attributer_name = data.get('name')
    
    if not attributer_name:
        return jsonify({'error': 'Attributer name is required'}), 400
    
    with DBSession() as session:
        # Correct usage of filter_by with keyword arguments
        attributer = session.query(ATTRIBUTE_CO).filter_by(name=attributer_name).first()
    
    if attributer:
        return jsonify({
            'attributerid': attributer.attributerid,
            'emailid': attributer.emailid
        })
    else:
        return jsonify({'error': 'Attributer not found'}), 404

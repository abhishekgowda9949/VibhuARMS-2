from flask import Blueprint, jsonify, render_template, request, session
from database import ATTRIBUTE_ALLOT, ATTRIBUTE_CO, DBSession

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
    
@allot_attributer_bp.route('/submit_allot_attribute', methods=['POST'])
def submit_allot_attribute():
    attributer_name = request.form['attributer_name']
    attributer_email = request.form['attributer_email']
    attributer_id = request.form['attributer_id']
    attribute_id = request.form['attribute']

    # Create an instance of the SQLAlchemy model
    new_entry = ATTRIBUTE_ALLOT(name=attributer_name, emailid=attributer_email, attributerid=attributer_id, attributeid=attribute_id)

    # Add to session and commit to save to database
    dbsession=DBSession()
    alloted_details = dbsession.query(ATTRIBUTE_ALLOT).filter(ATTRIBUTE_ALLOT.attributeid == attribute_id, ATTRIBUTE_ALLOT.attributerid == attributer_id).first()
    if alloted_details:
        return render_template('iqac/dashboard.html', messages ="Attributer Already Assigned!")
    else:
        dbsession.add(new_entry)
    dbsession.commit()
    dbsession.close()

    return render_template('iqac/dashboard.html', messages ="Attribute Assigned Successfully")

@allot_attributer_bp.route('/view_alloted_attribute')
def view_alloted_attribute():
    # Check if the user is logged in, if not redirect to login page
    if 'username' not in session:
        # Redirect to login page if user is not logged in
        return render_template('index.html', message="You are not logged in")

    # Open a new database session
    dbsession = DBSession()
    alloted_attribute = dbsession.query(ATTRIBUTE_ALLOT).all() # Fetch all assigned metrics
    
    # Close the database session
    dbsession.close()

    # Render the template with the fetched assigned metrics
    return render_template('iqac/view_alloted_attribute.html', alloted_attribute=alloted_attribute)
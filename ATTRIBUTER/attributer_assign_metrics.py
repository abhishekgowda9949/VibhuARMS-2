from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from database import ATTRIBUTE_ALLOT, DBSession, Metric_Details

attributer_assign_metrics_bp = Blueprint('attributer_assign_metrics', __name__)

@attributer_assign_metrics_bp.route('/attributer_assign_metrics')
def attributer_assign_metrics():
    if 'email' not in session:
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    dbsession = DBSession()
    attributer_emailid = session['email']
    attributer_alloc = dbsession.query(ATTRIBUTE_ALLOT).filter(ATTRIBUTE_ALLOT.emailid == attributer_emailid).all()
    
    attributer_alloc_ids = [alloc.attributeid for alloc in attributer_alloc]  # Collect all attribute IDs

    metrics = dbsession.query(Metric_Details).filter(Metric_Details.attribute_no.in_(attributer_alloc_ids)).all()
    dbsession.close()

    return render_template('attributer/attributer_assign_metrics.html', metrics=metrics)

@attributer_assign_metrics_bp.route('/fetch_metric_details', methods=['POST'])
def fetch_metric_details():
    metric_id = request.form.get('metric_id')
    if not metric_id:
        return jsonify({'error': 'Metric ID is required'}), 400

    dbsession = DBSession()
    metric = dbsession.query(Metric_Details).filter(Metric_Details.metric_no == metric_id).first()
    dbsession.close()

    if not metric:
        return jsonify({'error': 'Metric not found'}), 404

    metric_details = {
        'attribute_no': metric.attribute_no,
        'metric_no': metric.metric_no,
        'metric_description': metric.metric_description,
        'documents_required': metric.documents_required,
        'weightage': metric.weightage
    }

    return render_template('attributer/attributer_assign_metrics_2.html', metric=metric_details)

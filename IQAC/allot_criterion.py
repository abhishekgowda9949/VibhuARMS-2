from flask import Blueprint, render_template, request,session
allot_criterion_bp = Blueprint('allot_criterion', __name__)
from database import IQAC_C0, DBSession

@allot_criterion_bp.route('/allot_criterion')
def allot_criterion():
    return render_template('iqac/allot_criterion.html')
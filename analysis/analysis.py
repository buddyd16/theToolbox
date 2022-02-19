from flask import Blueprint, render_template

analysis_bp = Blueprint('analysis_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='analysis_assets')

@analysis_bp.route('/simplebeam', methods=['GET'])
def web_simplebeam():
    
    return render_template('analysis/simplebeam.html')
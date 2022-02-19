from flask import Blueprint, render_template

wood_bp = Blueprint('wood_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='wood_assets')

@wood_bp.route('/nds_stud_wall')
def wood_wall_web():

    return render_template('wood/nds_stud_wall.html')
from flask import Blueprint, render_template

foundations_bp = Blueprint('foundations_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='foundations_assets')


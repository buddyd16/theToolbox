from flask import Blueprint, render_template

masonry_bp = Blueprint('masonry_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='masonry_assets')


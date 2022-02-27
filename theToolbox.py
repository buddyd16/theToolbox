from flask import Flask, render_template, request, jsonify


# Blueprint Imports
from wood.wood import wood_bp
from concrete.concrete import concrete_bp
from foundations.foundations import foundations_bp
from analysis.analysis import analysis_bp
from steel.steel import steel_bp
from general.general import general_bp
from masonry.masonry import masonry_bp

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# from werkzeug.debug import DebuggedApplication
# app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

# app.debug = True

# Register Blueprints
app.register_blueprint(wood_bp, url_prefix='/wood')
app.register_blueprint(concrete_bp, url_prefix='/concrete')
app.register_blueprint(foundations_bp, url_prefix='/foundations')
app.register_blueprint(analysis_bp, url_prefix='/analysis')
app.register_blueprint(steel_bp, url_prefix='/steel')
app.register_blueprint(general_bp, url_prefix='/general')
app.register_blueprint(masonry_bp, url_prefix='/masonry')

# View
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title=None)

@app.route('/termsandconditions')
def terms():
    return render_template('termsandconditions.html', title='terms and conditions')

@app.route('/privacy-policy')
def privacy():
    return render_template('privacypolicy.html', title='privacy policy')

@app.route('/under_construction')
def not_ready():
    return render_template('under_construction.html', title='under construction')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.form.getlist("test")
        # print(request.form)
        # print(data)
    else:
        data = None

    return render_template('test.html', result=data, title='TEST')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
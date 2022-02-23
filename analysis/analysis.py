from flask import Blueprint, render_template, request

analysis_bp = Blueprint('analysis_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='analysis_assets')


@analysis_bp.route('/simplebeam', methods=['GET', 'POST'])
def web_simplebeam():
    if request.method == 'POST':

        form_data = request.form.getlist('distloadType')
        print(form_data)

        inputs = {"span": 20, "E": 29000.0, "I": 30.8, "OverL": 0, "OverR": 0, "fl": 0, "fr": 0,
                  "intSups": [10, 15],
                  "offPat": [0, 0, 0.5, 0],
                  "combos": 0,
                  "f1": 0.5,
                  "f2": 0.2,
                  "latReverse": 1,
                  "sls": [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]],
                  "distLoads": [[0, 1, 0, 1, 0, 1, "D"]],
                  "pointLoads": [[0, 0, "D"]],
                  "pointMoments": [[0, 0, "D"]]}
        results = None
    else:
        inputs = {"span": 20, "E": 29000.0, "I": 30.8, "OverL": 0, "OverR": 0, "fl": 0, "fr": 0,
                  "intSups": [10, 15],
                  "offPat": [0, 0, 0.5, 0],
                  "combos": 0,
                  "f1": 0.5,
                  "f2": 0.2,
                  "latReverse": 1,
                  "sls": [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]],
                  "distLoads": [[0, 1, 0, 1, 0, 1, "D"]],
                  "pointLoads": [[0, 0, "D"]],
                  "pointMoments": [[0, 0, "D"]]}

        results = 1

    return render_template('analysis/simplebeam.html', inputs=inputs, results=results)

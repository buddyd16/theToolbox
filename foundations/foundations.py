from flask import Blueprint, render_template, request

import foundations.foundations_compute as fnd_calc

foundations_bp = Blueprint('foundations_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='foundations_assets')


@foundations_bp.route('/ibc_unconstrained_pole_fnd', methods=['GET', 'POST'])
def unconstrained_pole_fnd_web():
    page_title = "IBC 2018 Unconstrained Pole Foundation"

    if request.method == 'POST':

        qh = float(request.form.get("qh_allow"))
        allow_180634 = int(request.form.get("allow_180634"))
        p = float(request.form.get("p"))
        h = float(request.form.get("h"))
        pole_shape = request.form.get("pole_shape")
        shape_size = float(request.form.get("shape_size"))
        dignore = float(request.form.get("d_ignore"))

        inputs = {"qh":qh,
                  "allow_180634":allow_180634,
                  "p":p,
                  "h":h,
                  "shape":pole_shape,
                  "shape_size":shape_size,
                  "dignore":dignore
                  }

        results = fnd_calc.web_ibc_18_1(inputs)

    else:
        inputs = {"qh":100,
                  "allow_180634":0,
                  "p":100,
                  "h":10,
                  "shape":"round",
                  "shape_size":24,
                  "dignore":1
                  }
        results = None

    return render_template('foundations/ibc_unconstrained_pole_fnd.html',
                            title=page_title, inputs=inputs, results=results)
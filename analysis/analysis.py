from flask import Blueprint, render_template, request

import analysis.analysis_compute as anal_calc

analysis_bp = Blueprint('analysis_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='analysis_assets')


@analysis_bp.route('/simplebeam', methods=['GET', 'POST'])
def web_simplebeam():
    if request.method == 'POST':
        
        # Get Geometry Inputs
        span = float(request.form.get('span'))
        em = float(request.form.get('spanE'))
        ixx = float(request.form.get('spanI'))
        
        # Disabled inputs return None
        if request.form.get('overhangLeft') is None:
            overL = 0
        else:
            overL = float(request.form.get('overhangLeft'))

        if request.form.get('overhangRight') is None:
            overR = 0
        else:
            overR = float(request.form.get('overhangRight'))

        # checkbox return none if not checked
        if request.form.get('fixedLeft') is None:
            fL = 0
        else:
            fL = 1
        
        # checkbox return none if not checked
        if request.form.get('fixedRight') is None:
            fR = 0
        else:
            fR = 1

        # Get the interior spans
        intSupports = request.form.getlist('interiorSupport')
        intSupports = [float(i) for i in intSupports]

        # Get the off pattern factors
        offPattern = [float(request.form.get('Lpatternfactor')),
                      float(request.form.get('Lrpatternfactor')),
                      float(request.form.get('Spatternfactor')),
                      float(request.form.get('Rpatternfactor'))]

        # Get ULS Load Combo Selection
        if request.form.get('designCombo') == 'IBC_ASD':
            ULScombos = 0
        else:
            ULScombos = 1

        # Get IBC f1 value
        IBC_f1 = float(request.form.get('IBC_f1'))

        # Get IBC f2 value
        IBC_f2 = float(request.form.get('IBC_f2'))

        # Get Lateral revesal choice
        latReverse  = int(request.form.get('latReverse'))

        # Get the User service combinations
        sls_D = request.form.getlist('Dsfactor')
        sls_F = request.form.getlist('Fsfactor')
        sls_L = request.form.getlist('Lsfactor')
        sls_H = request.form.getlist('Hsfactor')
        sls_Lr = request.form.getlist('Lrsfactor')
        sls_S = request.form.getlist('Ssfactor')
        sls_R = request.form.getlist('Rsfactor')
        sls_Wx = request.form.getlist('Wxsfactor')
        sls_Wy = request.form.getlist('Wysfactor')
        sls_Ex = request.form.getlist('Exsfactor')
        sls_Ey = request.form.getlist('Eysfactor')

        slsCombos = []
        for i, j in enumerate(sls_D):
            slsCombos.append([float(j),
                              float(sls_F[i]),
                              float(sls_L[i]),
                              float(sls_H[i]),
                              float(sls_Lr[i]),
                              float(sls_S[i]),
                              float(sls_R[i]),
                              float(sls_Wx[i]),
                              float(sls_Wy[i]),
                              float(sls_Ex[i]),
                              float(sls_Ey[i]),])

        # Get the Distributed Loads
        dl_w1 = request.form.getlist('w1')
        dl_t1 = request.form.getlist('trib1')
        dl_w2 = request.form.getlist('w2')
        dl_t2 = request.form.getlist('trib2')
        dl_a = request.form.getlist('dista')
        dl_b = request.form.getlist('distb')
        dl_k = request.form.getlist('distloadType')

        distLoads = []
        sumw = 0
        for i, j in enumerate(dl_w1):
            if float(j) != 0 or float(dl_w2[i]) != 0:
                sumw += 1

            distLoads.append([float(j),
                              float(dl_t1[i]),
                              float(dl_w2[i]),
                              float(dl_t2[i]),
                              float(dl_a[i]),
                              float(dl_b[i]),
                              dl_k[i]])

        # Get the Point Loads
        pl_p = request.form.getlist('pointLoad')
        pl_a = request.form.getlist('pointLoada')
        pl_k = request.form.getlist('pointloadType')

        pointLoads = []
        sump = 0
        for i, j in enumerate(pl_p):
            if float(j) != 0:
                sump += 1
            pointLoads.append([float(j),
                               float(pl_a[i]),
                               pl_k[i]])

        # Get the Moment Loads
        pm_m = request.form.getlist('pointMoment')
        pm_a = request.form.getlist('pointMomenta')
        pm_k = request.form.getlist('pointMomentType')

        momentLoads = []
        sumM = 0
        for i, j in enumerate(pm_m):
            if float(j) != 0:
                sumM += 1
            momentLoads.append([float(j),
                                float(pm_a[i]),
                                pm_k[i]])

        inputs = {"span": span,
                  "E": em, "I": ixx,
                  "OverL": overL, "OverR": overR,
                  "fl": fL, "fr": fR,
                  "intSups": intSupports,
                  "offPat": offPattern,
                  "combos": ULScombos,
                  "f1": IBC_f1,
                  "f2": IBC_f2,
                  "latReverse": latReverse,
                  "sls": slsCombos,
                  "distLoads": distLoads,
                  "pointLoads": pointLoads,
                  "pointMoments": momentLoads}

        # Quanity of non-0 loadings
        # If there are no loads then do nothing
        sumLoads = sumw + sump + sumM
        print(f'# Non-0 Loads: {sumLoads}')
        # send the inputs to the computation model
        if sumLoads > 0:
            computation = anal_calc.SimpleBeam(inputs)

            # store the results for use by the Jinja templating
            results = computation
        else:
            # store the results for use by the Jinja templating
            results = None

    else:
        inputs = {"span": 20,
                  "E": 29000.0, "I": 30.8,
                  "OverL": 0, "OverR": 0,
                  "fl": 0, "fr": 0,
                  "intSups": [0],
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

    return render_template('analysis/simplebeam.html',
                           inputs=inputs,
                           results=results)

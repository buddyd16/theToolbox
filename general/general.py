from flask import Blueprint, render_template, request

import general.general_compute as gen_calc

general_bp = Blueprint('general_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='general_assets')

@general_bp.route('/interpolate', methods=['GET','POST'])
def web_interpolate():
    return render_template('general/interpolate.html', title='interpolation')

@general_bp.route('/sectionprops', methods=['GET','POST'])
def web_section_props():
    if request.method == 'POST':    
        data_x = request.form.getlist("x")
        data_y = request.form.getlist("y")
        
        results,warnings,centroid, shape = gen_calc.sectionProps(data_x,data_y)
        
        # print(shape.Ivv)
        
        vertices = []
        
        for i,j in enumerate(data_x):
            
            vertices.append([i+1,j,data_y[i]])
        
    else:
        vertices = None
        results = None
        warnings = None
        centroid = '{x:0,y:0}'
        shape= None
        
    return render_template('general/sectionprops.html', vertices=vertices, result=results,warning=warnings, centroid = centroid, shape=shape, title='section properties')
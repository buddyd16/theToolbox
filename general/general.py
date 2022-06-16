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
       
        # New Work
        units = request.form.get("units")
        num_shapes = int(request.form.get("numshapes"))
        sections = []

        for i in range(num_shapes):
            shapestrg = "shape"+str(i+1)

            sections.append({"E": float(request.form.get(shapestrg+"E")),
                             "Fy": float(request.form.get(shapestrg+"Fy")),
                             "Solid": int(request.form.get(shapestrg+"Solid")),
                             "X": [float(i) for i in request.form.getlist(shapestrg+"x")],
                             "Y": [float(i) for i in request.form.getlist(shapestrg+"y")],
                             "Color": request.form.get(shapestrg+"Color")})
        
        inputs = {"units": units, "ShapesIn": sections,"ShapeCount": num_shapes}

        Results = gen_calc.sectionProps(sections)

        results = {"CompositeSection": Results[0], "Sections":Results[1]}

    else:
        
        default_shape = {"E":29000,"Fy":36,"Solid":1,"X":[0,1,1,0],"Y":[0,0,1,0],"Color": "#cc0000"}
        input_shapes = [default_shape]

        inputs = {"units": "imperial", "ShapesIn": input_shapes,"ShapeCount": len(input_shapes)}
        results = {"CompositeSection": None, "Sections": None}
        
    return render_template('general/sectionprops.html',
                            inputs = inputs ,  
                            results = results , 
                            title = 'section properties')
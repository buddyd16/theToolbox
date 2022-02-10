from flask import Flask, render_template, request, jsonify
import model as forms
import compute as calc
import aisc_database_class as aiscdb

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# View
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')
    
@app.route('/under_construction')
def not_ready():
    return render_template('under_construction.html')
    
@app.route('/tbeam', methods=['GET', 'POST'])
def web_tbeam():
    form = forms.InputForm(request.form)
    if request.method == 'POST' and form.validate():
        beam = calc.create_beam_section(form.B.data,
                                        form.H.data,
                                        form.Bf.data,
                                        form.Hf.data,
                                        form.fc.data,
                                        form.density.data)
                                        
        remaining_form_data = [form.cover.data,
                                form.fyf.data,
                                form.fys.data,
                                form.aggregate.data,
                                form.bar_v.data,
                                form.bottom_bar_size.data,
                                form.bottom_bar_layers.data,
                                form.bottom_bar_count.data,
                                form.top_bar_size.data,
                                form.top_bar_layers.data,
                                form.top_bar_count.data]
                                
        web_tbeam = calc.web_tbeam(beam,remaining_form_data)
        web_tbeam.run_analysis()
        
    else:
        beam = None
        web_tbeam = None


    return render_template('tbeam.html', form=form, beam=beam, web_beam=web_tbeam)

@app.route('/interpolate', methods=['GET','POST'])
def web_interpolate():
    form = forms.interpolate_form(request.form)
    
    if request.method == 'POST' and form.validate():
        result = calc.linear_interpolate(form.x1L.data,
                                        form.x2L.data,
                                        form.xL.data,
                                        form.y1L.data,
                                        form.y2L.data)
    
    else:
        result = None
    
    return render_template('interpolate.html',form=form, result=result)
    
@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':    
        data = request.form.getlist("test")
        # print(request.form)
        # print(data)
    else:
        data = None
    
    return render_template('test.html',result=data)

@app.route('/pt_profile', methods=['GET','POST'])
def web_pt_point():
    form = forms.pt_profile_form(request.form)
    
    if request.method == 'POST':
    
        e_prime = calc.pt_profile(form)

    else:
        e_prime = None
    
    return render_template('pt_profile.html',form=form, result=e_prime)

@app.route('/sectionprops', methods=['GET','POST'])
def web_section_props():
    if request.method == 'POST':    
        data_x = request.form.getlist("x")
        data_y = request.form.getlist("y")
        
        results,warnings,centroid, shape = calc.sectionProps(data_x,data_y)
        
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
        
    return render_template('sectionprops.html', vertices=vertices, result=results,warning=warnings, centroid = centroid, shape=shape)

@app.route('/aci_unit_width',methods=['GET','POST'])
def web_aci_unit_width():
    form = forms.aci_unit_width_form(request.form)
    
    if request.method == 'POST':
        
        results, detailed_results, warning = calc.aci_unit_width_section(form)
        
    else:
        results = None
        detailed_results = None
        warning = []
        
    return render_template('aci_unit_width.html', form=form, result=results,detailed=detailed_results, warning=warning)

@app.route('/elastic_weld_group', methods=['GET','POST'])
def web_elastic_weld_group():
    
    if request.method == 'POST':
        
        loadType = request.form['loadType']
        
        # print(loadType)
        
        xi = request.form.getlist("xi")
        yi = request.form.getlist("yi")
        xj = request.form.getlist("xj")
        yj = request.form.getlist("yj")
        
        segments = []
        for i,z in enumerate(xi):
        
            segments.append([float(z),float(yi[i]),float(xj[i]),float(yj[i])])
        
        # print(segments)
        
        loads_string = [request.form['fz'],request.form['fx'],request.form['fy'],request.form['mx'],request.form['my'],request.form['tz']]
        loads = [float(i) for i in loads_string]
        
        # print(loads)
        
        loadpoint = (request.form['loadPosition'], (float(request.form['user_x']),float(request.form['user_y']),float(request.form['user_z'])))
        
        # print(loadpoint)
        
        fexx = float(request.form['fexx'])
        
        segments, group, sigma, appliedLoad= calc.elastic_weld_analysis(segments, loads, loadpoint, loadType)
        
        throat_calc = calc.fillet_weld(sigma,fexx,loadType)
        
        loadInputs = [loadType,loads,loadpoint,fexx]
        
        centroid = group.centroid_web
    else:
        segments = None
        loadInputs = None
        sigma = None
        appliedLoad = None
        group = None
        throat_calc = None
        centroid = 0
    
    return render_template('weldgroup.html',segments=segments, loadInputs = loadInputs, sigma=sigma, appliedLoad=appliedLoad, weldgroup=group, throat=throat_calc, centroid=centroid)

@app.route('/simplebeam', methods=['GET'])
def web_simplebeam():
    
    return render_template('simplebeam.html')

@app.route('/steeldb')
def web_steeldb():

    return render_template('steeldb.html')

@app.route('/steeldbapi')
def api_aiscdb():
    
    shapeset = request.args.get("shapeset")
    shape = request.args.get("shape",None)
    shape_list = request.args.get("shapelist",None)
    filterprop = request.args.get("shapefilterprop",None)
    filterstart = request.args.get("shapefilterstart",None)
    filterend = request.args.get("shapefilterend",None)
    filterprop2 = request.args.get("shapefilterprop2",None)
    filterstart2 = request.args.get("shapefilterstart2",None)
    filterend2 = request.args.get("shapefilterend2",None)

    if filterprop != None:
        shapefilter = [filterprop, float(filterstart),float(filterend)]
    else:
        shapefilter = []
    
    if filterprop2 != None:
        shapefilter2 = [filterprop2, float(filterstart2),float(filterend2)]
    else:
        shapefilter2 = []
    
    print(shapefilter)

    db = aiscdb.aisc_15th_database()
    
    # Get Full Shape Set
    if shapeset == "WF":
        list,data,dictionary = db.WF(shapefilter, shapefilter2)
    elif shapeset == "PIPE":
        list,data,dictionary = db.PIPE(shapefilter, shapefilter2)
    elif shapeset == "C":
        list,data,dictionary = db.C(shapefilter, shapefilter2)
    elif shapeset == "HSS_RND":
        list,data,dictionary = db.HSS_RND(shapefilter, shapefilter2)
    elif shapeset == "MC":
        list,data,dictionary = db.MC(shapefilter, shapefilter2)
    elif shapeset == "HSS_RECT":
        list,data,dictionary = db.HSS_RECT(shapefilter, shapefilter2)
    elif shapeset == "HP":
        list,data,dictionary = db.HP(shapefilter, shapefilter2)
    elif shapeset == "M":
        list,data,dictionary = db.M(shapefilter, shapefilter2)
    elif shapeset == "L":
        list,data,dictionary = db.L(shapefilter, shapefilter2)
    elif shapeset == "ST":
        list,data,dictionary = db.ST(shapefilter, shapefilter2)
    elif shapeset == "HSS_SQR":
        list,data,dictionary = db.HSS_SQR(shapefilter, shapefilter2)
    elif shapeset == "MT":
        list,data,dictionary = db.MT(shapefilter, shapefilter2)
    elif shapeset == "S":
        list,data,dictionary = db.S(shapefilter, shapefilter2)
    elif shapeset == "WT":
        list,data,dictionary = db.WT(shapefilter, shapefilter2)
    elif shapeset == "LL":
        list,data,dictionary = db.LL(shapefilter, shapefilter2)
    else:
        list = []
        data = []
        dictionary = {}
    
    # Filter the dictionary to the specific requested shape
    if shape != None:
        dictionary = next((item for item in dictionary if item["AISC_Manual_Label"][0]==''+shape+''),{})
    
    if shape_list == "1":
        return jsonify(list)
    else:
        return jsonify(dictionary)

@app.route('/aci_development')
def aci_development_web():

    return render_template("aci_development.html")

@app.route('/aci_corbel')
def aci_corbel_web():

    return render_template("aci_corbel.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
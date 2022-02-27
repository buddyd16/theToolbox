from flask import Blueprint, render_template, request, jsonify

import steel.aisc_database_class as aiscdb
import steel.steel_compute as steel_calc


steel_bp = Blueprint('steel_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='steel_assets')

@steel_bp.route('/steeldb')
def web_steeldb():

    return render_template('steel/steeldb.html', title='steel shape database')

@steel_bp.route('/steeldbapi')
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

@steel_bp.route('/elastic_weld_group', methods=['GET','POST'])
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
        
        segments, group, sigma, appliedLoad= steel_calc.elastic_weld_analysis(segments, loads, loadpoint, loadType)
        
        throat_calc = steel_calc.fillet_weld(sigma,fexx,loadType)
        
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
    
    return render_template('steel/weldgroup.html',segments=segments, loadInputs = loadInputs, sigma=sigma, appliedLoad=appliedLoad, weldgroup=group, throat=throat_calc, centroid=centroid, title='elastic weld group')
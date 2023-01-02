from unittest.mock import NonCallableMagicMock
from flask import Blueprint, render_template, request, jsonify

import wood.nds_database as ndsdb

wood_bp = Blueprint('wood_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='wood_assets')

@wood_bp.route('/nds_stud_wall', methods=['GET', 'POST'])
def wood_wall_web():
    if request.method == 'POST':

        geometry = {"b": int(request.form.get("stud_b")),
                    "d": int(request.form.get("stud_d")),
                    "plys": int(request.form.get("stud_plys")),
                    "spacing": float(request.form.get("stud_spacing")),
                    "height": float(request.form.get("wall_height")),
                    "subtract plates": int(request.form.get("subtract_plates",0)),
                    "number of plates": int(request.form.get("num_plates_subtract")),
                    "plate crushing": int(request.form.get("plate_crushing",0))}

        stud = {"ndstable": request.form.get("nds_supp_table_select"),
                "species": request.form.get("nds_species_select"),
                "grade": request.form.get("nds_grade_select"),
                "Fb": float(request.form.get("fb_input")),
                "Ft": float(request.form.get("ft_input")),
                "Fv": float(request.form.get("fv_input")),
                "Fcp": float(request.form.get("fcp_input")),
                "Fc": float(request.form.get("fc_input")),
                "E": float(request.form.get("E_input")),
                "Emin": float(request.form.get("Emin_input")),
                "G": float(request.form.get("G_input")),
                "Grading Agency": request.form.get("agency_input")}

        plate = {"ndstable": request.form.get("nds_supp_table_select_plate"),
                    "species": request.form.get("nds_species_select_plate"),
                    "grade": request.form.get("nds_grade_select_plate"),
                    "Fb": float(request.form.get("fb_input_plate")),
                    "Ft": float(request.form.get("ft_input_plate")),
                    "Fv": float(request.form.get("fv_input_plate")),
                    "Fcp": float(request.form.get("fcp_input_plate")),
                    "Fc": float(request.form.get("fc_input_plate")),
                    "E": float(request.form.get("E_input_plate")),
                    "Emin": float(request.form.get("Emin_input_plate")),
                    "G": float(request.form.get("G_input_plate")),
                    "Grading Agency": request.form.get("agency_input_plate")}

        environment = {"moisture content": float(request.form.get("moisture_content")),
                        "temperature": float(request.form.get("service_temperature")),
                        "incised": int(request.form.get("incised_yn",0)),
                        "frt": int(request.form.get("frt_yn",0)),
                        "Cfrt": {"Cfrt_fb": float(request.form.get("c_frt_fb")),
                                    "Cfrt_ft": float(request.form.get("c_frt_ft")),
                                    "Cfrt_fv": float(request.form.get("c_frt_fv")),
                                    "Cfrt_fcp": float(request.form.get("c_frt_fcp")),
                                    "Cfrt_fc": float(request.form.get("c_frt_fc")),
                                    "Cfrt_E": float(request.form.get("c_frt_e")),
                                    "Cfrt_Emin": float(request.form.get("c_frt_emin")),
                                    "Cfrt_G": float(request.form.get("c_frt_g"))}}

        loadbracing = {"pressure": float(request.form.get("lateral_pressure")),
                        "Cd": float(request.form.get("cd_select")),
                        "min ecc": int(request.form.get("min_e_yn",0)),
                        "sheathing": int(request.form.get("sheathing_select")),
                        "blocking spacing": float(request.form.get("blocking_input"))}

        results = None
    else:
        geometry = {"b": 2,
                    "d": 4,
                    "plys": 1,
                    "spacing": 16,
                    "height": 10,
                    "subtract plates": 0,
                    "number of plates": 0,
                    "plate crushing": 1}

        stud = {"ndstable": "USER",
                "species": "USER",
                "grade": "USER",
                "Fb": 1,
                "Ft": 1,
                "Fv": 1,
                "Fcp": 1,
                "Fc": 1,
                "E": 1,
                "Emin": 1,
                "G": 1,
                "Grading Agency": "USER"}

        plate = {"ndstable": "USER",
                    "species": "USER",
                    "grade": "USER",
                    "Fb": 1,
                    "Ft": 1,
                    "Fv": 1,
                    "Fcp": 1,
                    "Fc": 1,
                    "E": 1,
                    "Emin": 1,
                    "G": 1,
                    "Grading Agency": "USER"}

        environment = {"moisture content": 19,
                        "temperature": 50,
                        "incised": 0,
                        "frt": 0,
                        "Cfrt": {"Cfrt_fb": 1,
                                    "Cfrt_ft": 1,
                                    "Cfrt_fv": 1,
                                    "Cfrt_fcp": 1,
                                    "Cfrt_fc": 1,
                                    "Cfrt_E": 1,
                                    "Cfrt_Emin": 1,
                                    "Cfrt_G": 1}}

        loadbracing = {"pressure": 5,
                        "Cd": 1,
                        "min ecc": 0,
                        "sheathing": 1,
                        "blocking spacing": 4}
        results = None

    inputs = {"geometry": geometry,
                "stud": stud,
                "plate": plate,
                "environment": environment,
                "loadbracing":loadbracing}

    print("-"*100)
    print("Inputs Echo:")
    print(inputs)
    print("-"*100)

    return render_template('wood/nds_stud_wall.html', 
                            title = 'wood wall',
                            inputs = inputs, 
                            results = results)

@wood_bp.route('/ndsdb_api')
def api_ndsdb():
    
    db = ndsdb.NDSDatabase()
    
    table = request.args.get("table")
    keys_only = request.args.get("keys")
    species = request.args.get("species")
    grade = request.args.get("grade")
    if request.args.get("depth") == None:
        shapeD = 1
    else:
        shapeD = float(request.args.get("depth"))
    
    print(table)
    print(keys_only)
    print(species)
    print(grade)
    
    if table=="4A":
        #print(db.table_4a.keys())
        dict_out = db.table_4a
    elif table=="4B":
        #print(db.table_4b.keys())
        dict_out = db.table_4b
    else:
        print("No Table Selected")
        dict_out={}
    
    if keys_only:
        if species != None:
            grades_out = []

            grades = dict_out[species].keys()

            for grade in grades:

                size_classes = dict_out[species][grade].keys()

                for size_class in size_classes:

                    d_max = dict_out[species][grade][size_class]['Drange'][1]
                    d_min = dict_out[species][grade][size_class]['Drange'][0]
                    if d_min <= shapeD and d_max >= shapeD:
                        grades_out.append(grade)

            return jsonify(grades_out)
        else:
            return jsonify(list(dict_out.keys()))
    else:
        if species != None and grade != None:
            size_classes = dict_out[species][grade].keys()
            for size_class in size_classes:
                    d_max = dict_out[species][grade][size_class]['Drange'][1]
                    d_min = dict_out[species][grade][size_class]['Drange'][0]
                    if d_min <= shapeD and d_max >= shapeD:
                        size = size_class
            return jsonify(dict_out[species][grade][size])

        if species != None and grade == None:
            return jsonify(dict_out[species])
        else:
            return jsonify(dict_out)
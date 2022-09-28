from unittest.mock import NonCallableMagicMock
from flask import Blueprint, render_template, request, jsonify

import wood.nds_database as ndsdb

wood_bp = Blueprint('wood_bp', __name__,
            template_folder='templates',
            static_folder='static', static_url_path='wood_assets')

@wood_bp.route('/nds_stud_wall')
def wood_wall_web():

    return render_template('wood/nds_stud_wall.html', title='wood wall')

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
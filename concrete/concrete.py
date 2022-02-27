from flask import Blueprint, render_template, request

import concrete.concrete_model as cip_model
import concrete.concrete_compute as cip_calc

concrete_bp = Blueprint('concrete_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='concrete_assets')


@concrete_bp.route('/tbeam', methods=['GET', 'POST'])
def web_tbeam():
    form = cip_model.InputForm(request.form)
    if request.method == 'POST' and form.validate():
        beam = cip_calc.create_beam_section(form.B.data,
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

        web_tbeam = cip_calc.web_tbeam(beam, remaining_form_data)
        web_tbeam.run_analysis()

    else:
        beam = None
        web_tbeam = None

    return render_template('concrete/tbeam.html', form=form, beam=beam, web_beam=web_tbeam, title='CIP T Beam')


@concrete_bp.route('/pt_profile', methods=['GET', 'POST'])
def web_pt_point():
    form = cip_model.pt_profile_form(request.form)

    if request.method == 'POST':

        e_prime = cip_calc.pt_profile(form)

    else:
        e_prime = None

    return render_template('concrete/pt_profile.html', form=form, result=e_prime, title='PT Profile Low Point')


@concrete_bp.route('/aci_unit_width', methods=['GET', 'POST'])
def web_aci_unit_width():
    form = cip_model.aci_unit_width_form(request.form)

    if request.method == 'POST':

        results, detailed_results, warning = cip_calc.aci_unit_width_section(
            form)

    else:
        results = None
        detailed_results = None
        warning = []

    return render_template('concrete/aci_unit_width.html', form=form, result=results, detailed=detailed_results, warning=warning, title="ACI Unit Width")


@concrete_bp.route('/aci_development')
def aci_development_web():

    return render_template("concrete/aci_development.html", title="ACI Development Length")


@concrete_bp.route('/aci_corbel')
def aci_corbel_web():

    return render_template("concrete/aci_corbel.html", title="ACI Corbel")

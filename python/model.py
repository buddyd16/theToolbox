from wtforms import Form, FloatField, SelectField, validators
from math import pi

class InputForm(Form):

    densities = ["145","150"]
    fys = ["60","40","80"]
    aggs = ["0.75","1.0"]
    bars_v = ["0","3","4","5"]
    bars = ["3","4","5","6","7","8","9","10","11","14","18"]
    layers = ["1","2","3","4"]
    layerst = ["0","1","2","3","4"]
    
    B = FloatField(
        label='Beam Web Width (in):', default=12.0,
        validators=[validators.InputRequired()])
    H = FloatField(
        label='Beam Total Height (in):', default=24.0,
        validators=[validators.InputRequired()])
    Bf = FloatField(
        label='Beam Flange Width (in):', default=0.0,
        validators=[validators.InputRequired()])
    Hf = FloatField(
        label='Beam Flange Thickness(in):', default=0.0,
        validators=[validators.InputRequired()])
    fc = FloatField(
        label="F'c (psi):", default=4000.0,
        validators=[validators.InputRequired()])
    density = SelectField('Density (pcf):', choices=densities)
    cover = FloatField(
        label='Cover (in):', default=1.5,
        validators=[validators.InputRequired()])
    fyf = SelectField('Fy,main bars (ksi):', choices=fys)
    fys = SelectField('Fy,shear bars (ksi):', choices=fys)
    aggregate = SelectField('Aggregate Size (in):', choices=aggs)
    bar_v = SelectField('Shear Bar Size:', choices=bars_v)
    bottom_bar_size = SelectField('Bottom Bar Size:', choices=bars)
    bottom_bar_layers = SelectField('Bottom Bar Layers:', choices=layers)
    bottom_bar_count = FloatField(
        label='Bottom Bars per layer:', default=1.5,
        validators=[validators.InputRequired()])
    top_bar_size = SelectField('Top Bar Size:', choices=bars)
    top_bar_layers = SelectField('Top Bar Layers:', choices=layerst)
    top_bar_count = FloatField(
        label='Top Bars per layer:', default=1.5,
        validators=[validators.InputRequired()])        

class interpolate_form(Form):

    x1L = FloatField(
        label='x1:', default=0,
        validators=[validators.InputRequired()])
    xL = FloatField(
        label='x:', default=0,
        validators=[validators.InputRequired()])
    x2L = FloatField(
        label='x2:', default=0,
        validators=[validators.InputRequired()])
    y1L = FloatField(
        label='y1:', default=0,
        validators=[validators.InputRequired()])
    y2L = FloatField(
        label='y2:', default=0,
        validators=[validators.InputRequired()])

class pt_profile_form(Form):
    densities = ["145","150"]
    t_slab = FloatField(
            label='t,slab (in)', default=8.0,
            validators=[validators.InputRequired()])
    density = SelectField('Density (pcf):', choices=densities)
    percent_balance = FloatField(
            label='Percent of Self Weight to Balance (%):', default=80.0,
            validators=[validators.InputRequired()])
    pt_point_left = FloatField(
            label='Left Profile Point Elevation from Soffit (in):', default=7,
            validators=[validators.InputRequired()])
    pt_point_right = FloatField(
            label='Right Profile Point Elevation from Soffit (in):', default=7,
            validators=[validators.InputRequired()])
    span = FloatField(
            label='Span Length (ft):', default=25.5,
            validators=[validators.InputRequired()])
    width = FloatField(
            label='Span Width (ft):', default=25.5,
            validators=[validators.InputRequired()])
    fpu = FloatField(
            label='PT Ultimate Tensile Strength (Fpu) (ksi):', default=270.0,
            validators=[validators.InputRequired()])
    loss_psi = FloatField(
            label='Anticipated Stress Loss (ksi):', default=15.0,
            validators=[validators.InputRequired()])
    tendon_area = FloatField(
            label='PT Tendon Area (Aps) (in^2):', default=0.153,
            validators=[validators.InputRequired()])
    num_tendon = FloatField(
            label='Number of Tendons:', default=5.0,
            validators=[validators.InputRequired()])

class aci_unit_width_form(Form):
    as_mins = ["Beam","One-Way Slab","Two-Way Slab","Wall"]
    cover_to = ["Bar Centroid","Bar Surface"]
    
    as_min_consider = SelectField('Section type for As,min:', choices=as_mins)
    
    f_prime_c_psi =  FloatField(
            label="F'c (psi)", default=4500.0,
            validators=[validators.InputRequired()])
            
    cover_in =  FloatField(
            label="Cover (in)", default=3.0,
            validators=[validators.InputRequired()])
            
    cover_to_select = SelectField('Cover is measured to:', choices=cover_to)
    
    h_in =  FloatField(
            label="H (in)", default=12.0,
            validators=[validators.InputRequired()])
            
    mu_ftkip =  FloatField(
            label="Mu (ft-kips/ft)", default=12.0,
            validators=[validators.InputRequired()])
            
    vu_kip =  FloatField(
            label="Vu (kips/ft)", default=6.0,
            validators=[validators.InputRequired()])
    
    agg_size = FloatField(
            label="Aggregate Size (in)", default=1.0,
            validators=[validators.InputRequired()])
    
    spacing_module = FloatField(
            label="Spacing Module (in)", default=3,
            validators=[validators.InputRequired()])
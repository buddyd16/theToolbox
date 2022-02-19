import concrete.concrete_beam_classes as cbc
import math

def create_beam_section(b_in, h_in, bf_in, hf_in, f_prime_c_psi, density_pcf):
    b = float(b_in)
    h = float(h_in)
    bf = float(bf_in)
    hf = float(hf_in)
    fc = float(f_prime_c_psi)
    density = float(density_pcf)
    
    beam = cbc.t_beam(b, h, 0, 0, 0, 0, bf, hf, fc,density)
    
    return beam

class web_tbeam:
    def __init__(self, beam, inputs=[]):
        self.beamsection = beam
        
        # Initialize Warning List
        self.warnings = []
        self.errors = []
        
        # Initialize web output list
        # makes the output iterable
        
        self.detailed_output = []
        self.primary_output = []
        self.geometry_output = []
        self.flexure_output = []
        self.shear_output = []
        self.torsion_output = []
        
        # set cover
        self.cover_in = float(inputs[0])
        
        # set aggregate_size_in
        self.aggregate_size_in = float(inputs[3])
        
        # Set Shear Bar Size and Fy
        self.shear_bars_fy = cbc.reinforcement(float(inputs[2]))
        self.shear_bar = self.shear_bars_fy.bar[int(inputs[4])]
        
        #print(self.shear_bar)
        
        # Set Flexural Bar Sizes and Fy
        self.flexural_bars_fy = cbc.reinforcement(float(inputs[1]))
        self.bottom_bar_size = int(inputs[5])
        self.top_bar_size = int(inputs[8])

        self.bottom_bar = self.flexural_bars_fy.bar[self.bottom_bar_size]
        self.top_bar = self.flexural_bars_fy.bar[self.top_bar_size]
        
        # Determine Minimum amount of outer layer bottom bars and
        # max bars that fit in a layer
        self.min_outer_bars = self.beamsection.min_bars_bottom_layer(self.bottom_bar,self.cover_in,self.shear_bar, self.flexural_bars_fy.fy_psi)
        self.max_bottom_bars_per_Layer = self.beamsection.max_bars_layer(self.bottom_bar,self.cover_in,self.shear_bar, self.aggregate_size_in)
        self.max_top_bars_per_Layer = self.beamsection.max_bars_layer(self.top_bar,self.cover_in,self.shear_bar, self.aggregate_size_in)
        
        self.detailed_output.append(["Min. # of Outer Bars =",self.min_outer_bars,"",""])
        self.detailed_output.append(["Max. # of Bars per bottom layer =",self.max_bottom_bars_per_Layer,"",""])
        self.detailed_output.append(["Max. # of Bars per top layer =",self.max_top_bars_per_Layer,"",""])
        
        # set bars per layer
        self.bottom_bars_per_layer = float(inputs[7])
        self.top_bars_per_layer = float(inputs[10])
        
        if self.bottom_bars_per_layer < self.min_outer_bars:
            self.warnings.append("Bottom bar quantity may not satisfy crack control requirements.")
            
        if self.bottom_bars_per_layer > self.max_bottom_bars_per_Layer:
            self.warnings.append("Bottom bar quantity may not fit in section.")
        
        if self.top_bars_per_layer > self.max_top_bars_per_Layer:
            self.warnings.append("Top bar quantity may not fit in section.")
        
        # set bottom and top bar layer quantities
        self.num_bottom_layers = int(inputs[6])
        self.num_top_layers = int(inputs[9])
    
    def run_analysis(self):
        
        # initialize collection arrays
        top_bars_array = []
        top_bars_per_layer_array = []
        flexural_bars_array = []
        flexural_bars_as_array = []
        flexural_bars_d_array = []
        flexural_bars_per_layer_array = []

        bottom_bars_moment_ftkips_array = []

        top_bars_moment_ftkips_array = []

        flexural_bars_cg = 0

        fy_psi = self.flexural_bars_fy.fy_psi
        Es_psi = self.flexural_bars_fy.Es_psi
        
        self.detailed_output.append(["E<sub>s</sub> =",Es_psi/1000.0,"ksi","Steel Modulus of Elasticity"])
        
        # Set bottom bar arrays
        bottom_bars_array = [self.bottom_bar]*self.num_bottom_layers
        bottom_bars_per_layer_array = [self.bottom_bars_per_layer]*self.num_bottom_layers
        
        # create bottom bas as and d arrays
        bottom_bars_as_array, bottom_bars_d_array,self.bottom_bars_cg = self.beamsection.flexural_bottom_bars_automatic_by_layers(bottom_bars_array,bottom_bars_per_layer_array,self.cover_in,self.shear_bar)
        
        # Set top bar arrays
        if self.num_top_layers==0:
            top_bars_array.append(0)
            top_bars_per_layer_array.append(0)
            top_bars_as_array = [0]
            top_bars_d_array = [0]
            top_bars_cg = 0
            
        else:
            top_bars_array = [self.top_bar]*self.num_top_layers
            top_bars_per_layer_array = [self.top_bars_per_layer]*self.num_top_layers
            
            top_bars_as_array, top_bars_d_array, top_bars_cg = self.beamsection.flexural_top_bars_automatic_by_layers(top_bars_array,top_bars_per_layer_array,self.cover_in,self.shear_bar)
        
        # combine bar arrays for entry into beam functions
        if top_bars_array[0]==0:
            flexural_bars_array = bottom_bars_array
            flexural_bars_as_array = bottom_bars_as_array
            flexural_bars_d_array = bottom_bars_d_array
            flexural_bars_per_layer_array = bottom_bars_per_layer_array
        else:
            flexural_bars_array = bottom_bars_array + top_bars_array
            flexural_bars_as_array = bottom_bars_as_array + top_bars_as_array
            flexural_bars_d_array = bottom_bars_d_array + top_bars_d_array
            flexural_bars_per_layer_array = bottom_bars_per_layer_array + top_bars_per_layer_array
        
        # Compute total area of steel
        total_as = sum(flexural_bars_as_array)
        total_as_d = 0
        i=0
        for i in range(len(flexural_bars_as_array)):
            total_as_d = total_as_d + (flexural_bars_as_array[i]*flexural_bars_d_array[i])

        self.flexural_bars_cg = total_as_d/total_as
        
        self.minas = self.beamsection.as_min(self.bottom_bars_cg,fy_psi)
        
        if self.minas > sum(bottom_bars_as_array):
            asweb = round(sum(bottom_bars_as_array),3)
            minasweb = round(self.minas,3)
            self.errors.append(f"A<sub>s,min</sub> of {minasweb} in<sup>2</sup> not satisfied. A<sub>s,provided</sub> = {asweb} in<sup>2</sup>")
        
        # Compute the PNA
        self.PNA = self.beamsection.find_pna(flexural_bars_as_array,flexural_bars_d_array,flexural_bars_cg,fy_psi,Es_psi)
        
        
        # Bottom Bar strains and Forces
        bottom_bars_strain_array, bottom_bars_stress_psi_array, bottom_bars_force_lbs_array, total_bottom_force = self.beamsection.strain_compatibility_steel(bottom_bars_as_array,bottom_bars_d_array,self.PNA,fy_psi,Es_psi)
        
        
        # Table for Bottom Bars for Web output
        self.bottom_bar_table = [[i,j,round(k,3),round(l,4),round(m*1000.0,3),round(n,3),round(o,3)] for i,j,k,l,m,n,o in zip(bottom_bars_array,bottom_bars_per_layer_array,bottom_bars_as_array,bottom_bars_d_array,bottom_bars_strain_array, bottom_bars_stress_psi_array, bottom_bars_force_lbs_array)]
        
        # Top Bar strains and forces
        if top_bars_array[0]==0:
            total_top_force = 0
            top_bars_strain_array = [0]
            top_bars_stress_psi_array = [0]
            top_bars_force_lbs_array = [0]
        else:
            top_bars_strain_array, top_bars_stress_psi_array, top_bars_force_lbs_array, total_top_force = self.beamsection.strain_compatibility_steel(top_bars_as_array,top_bars_d_array,self.PNA,fy_psi,Es_psi)
        
        # Table for top Bars for Web output
        self.top_bar_table = [[i,j,round(k,3),round(l,4),round(m*1000.0,3),round(n,3),round(o,3)] for i,j,k,l,m,n,o in zip(top_bars_array,top_bars_per_layer_array,top_bars_as_array,top_bars_d_array,top_bars_strain_array, top_bars_stress_psi_array, top_bars_force_lbs_array)]
        
        # Concrete Forces
        concrete_compression_force_lbs, concrete_compression_force_cg_in = self.beamsection.strain_compatibility_concrete(self.PNA)
        
        
        # Error checks for failed PNA and Tension Controlled Section
        if 1 - (abs(concrete_compression_force_lbs) / abs(total_top_force + total_bottom_force)) >= 0.00001:
            self.errors.append("Solver for PNA Failed. Notify Developer!")
            
        if bottom_bars_strain_array[0]<0.004:
            self.errors.append("Section is not tension controlled!")
            
        # Compute Capacities - do this regardless of the errors and warnings above
        phi, nominal_moment, ultimate_moment = self.beamsection.moment_capacity_inlbs(flexural_bars_as_array,flexural_bars_d_array,flexural_bars_cg,self.PNA,fy_psi,Es_psi)
        phiv, vc, phivc, vsmax, vnmax, phivnmax = self.beamsection.concrete_shear_capacity_lbs(self.bottom_bars_cg,self.shear_bars_fy.fy_psi,self.shear_bar[1])
        phit, Acp, Pcp, t_threshold, phit_threshold, aop_status = self.beamsection.concrete_threshold_torsion_inlbs()

        a = self.beamsection.beta1 * self.PNA
        
        # Error Checking for bar forces 
        if min(bottom_bars_force_lbs_array) < 0:
            self.errors.append("Not all bottom bar layers are in tension. Remove a bottom bar layer")
        
        if max(top_bars_force_lbs_array) > 0:
            self.errors.append("Not all top bar layers are in compression. Remove a top bar layer")
        
        # compute I,cracked
        i_cracked_in4, cracked_na = self.beamsection.cracked_moment_of_inertia_in4(flexural_bars_as_array,flexural_bars_d_array,Es_psi)
        
        # create self variables for output reference
        self.icracked = i_cracked_in4
        self.a = a
        
        self.phi = phi
        self.mn_ftkips = nominal_moment/(12*1000.0)
        self.mu_ftkips = ultimate_moment/(12*1000.0)
        
        self.phiv = phiv
        self.vc_kips = vc/1000.0

        #CHECK MU VS CRACKING MOMENT
        if self.mu_ftkips<=self.beamsection.Mcrack_ftkips:
            self.warnings.append("&#934;<sub>b</sub>M<sub>n</sub> &#8804; M<sub>cr</sub> , ductile failure is unlikely")
        
        self.errors_count = len(self.errors)
        self.warnings_count = len(self.warnings)
        
        #print(self.errors,self.warnings)
        
        check = (total_bottom_force-((-1*total_top_force)+concrete_compression_force_lbs))
        
        # Compile Flexure Results for Web Output
        self.flexure_output.append(["A<sub>s,min</sub> =",round(self.minas,3),"in<sup>2</sup>","Minimum Required Steel Area"])
        self.flexure_output.append(["A<sub>s</sub> =",round(sum(bottom_bars_as_array),3),"in<sup>2</sup>","Area of Bottom (Tension) Flexural Steel"])
        self.flexure_output.append(["d =",round(self.bottom_bars_cg,3),"in","Distance to centroid of tension steel"])
        self.flexure_output.append(["A'<sub>s</sub> =",round(sum(top_bars_as_array),3),"in<sup>2</sup>","Area of Top (Compression) Flexural Steel"])
        self.flexure_output.append(["d' =",round(top_bars_cg,3),"in","Distance to centroid of compression steel"])
        self.flexure_output.append(["PNA = c =",round(self.PNA,3),"in","Depth to Plastic Neutral Axis"])
        self.flexure_output.append(["&#946;<sub>1</sub> =",round(self.beamsection.beta1,3),"","Whitney Stress Block Factor"])
        self.flexure_output.append(["a =",round(self.a,3),"in","Depth of Whitney Block = &#946;<sub>1</sub>*c"])
        self.flexure_output.append(["Ts = ",round(total_bottom_force,3),"lbs","Sum of A<sub>s</sub>*&#963;<sub>s</sub> for bottom reinf."])
        self.flexure_output.append(["Cs = ",round(-1*total_top_force,3),"lbs","Sum of A'<sub>s</sub>*&#963;'<sub>s</sub> for top reinf."])
        self.flexure_output.append(["Cc = ",round(concrete_compression_force_lbs,3),"lbs","0.85*F'<sub>c</sub>*Area of Compression Block"])
        self.flexure_output.append(["Ts - (Cs+Cc) =",f"{check:.2E}","","Error of Iterative PNA Solution"])
        self.flexure_output.append(["&#934;<sub>b</sub> =", round(phi,4),"","Moment Strength Reduction Factor"])
        self.flexure_output.append(["M<sub>n</sub> =", round(self.mn_ftkips,3),"ft-kips","Nominal Moment Capacity"])
        self.flexure_output.append(["&#934;<sub>b</sub>M<sub>n</sub> =", round(self.mu_ftkips,3),"ft-kips","Ultimate Moment Capacity"])
        self.flexure_output.append(["M<sub>cr</sub> =",round(self.beamsection.Mcrack_ftkips,3),"ft-kips","Cracking Moment"])
        self.flexure_output.append(["F<sub>r</sub> =",round(self.beamsection.fr_psi,3),"psi","Rupture Stress (Stress that initiates tensile cracking)"])
        

        
        # Compile Shear Results for Web Output
        self.shear_output.append(["d =",round(self.bottom_bars_cg,3),"in","Distance to centroid of tension steel"])
        self.shear_output.append(["&#934;<sub>v</sub> =", phiv,"","Shear Strength Reduction Factor"])
        self.shear_output.append(["V<sub>c</sub> =", round(self.vc_kips,3),"kips","Nominal Concrete Shear Capacity"])
        self.shear_output.append(["&#934;<sub>v</sub>V<sub>c</sub> =", round(self.vc_kips*phiv,3),"kips","Ultimate Concrete Shear Capacity"])
        self.shear_output.append(["0.5*&#934;<sub>v</sub>V<sub>c</sub> =", round(0.5*self.vc_kips*phiv,3),"kips","1/2 Ultimate Concrete Shear Capacity"])
        
        
        if self.shear_bar[0]==0:
            self.vn_max = round(self.vc_kips*phiv,3)
            self.phi_vn_max = f"&#934;<sub>v</sub>V<sub>n,max</sub> = {self.vn_max} kips"
            
            self.shear_output.append(["&#934;<sub>v</sub>V<sub>n</sub> =", round(self.vc_kips*phiv,3),"kips","Ultimate Section Shear Capacity (no shear bars)"])
        else:
            self.vn_max = round(vnmax/1000.0,3)
            self.phi_vn_max = round(phiv*vnmax/1000.0,3)
            self.phi_vn_max = f"&#934;<sub>v</sub>V<sub>n,max</sub> = {self.phi_vn_max} kips"
            
            self.shear_output.append(["V<sub>s,max</sub> =", round(vsmax/1000.0,3),"kips","Maximum Allowed Nominal Steel Shear Capacity"])
            self.shear_output.append(["V<sub>n,max</sub>= V<sub>c</sub>+V<sub>s,max</sub> =", round(vnmax/1000.0,3),"kips","Maximum Allowed Nominal Section Shear Capacity"])
            self.shear_output.append(["&#934;<sub>v</sub>V<sub>n,max</sub> =", round(phiv*vnmax/1000.0,3),"kips","Maximum Allowed Ultimate Section Shear Capacity"])
            self.shear_output.append(["S<sub>max</sub> =",round(self.beamsection.max_shear_spacing_in,3),"in","Maximum vertical stirrup spacing"])
            self.shear_output.append(["S'<sub>max</sub> =",round(0.5*self.beamsection.max_shear_spacing_in,3),"in","Maximum vertical stirrup spacing, V<sub>s,req</sub>&#8805;0.5*V<sub>s,max</sub>"])
            self.shear_output.append(["A<sub>v,min</sub> =", f"{self.beamsection.av_min_s:.3f}*S","in<sup>2</sup>","Minimum shear reinf. area"])
            self.shear_output.append(["A<sub>v,min</sub> @ S<sub>max</sub> =", round(self.beamsection.max_shear_spacing_in*self.beamsection.av_min_s,3),"in<sup>2</sup>","Minimum shear reinf. area @ S<sub>max</sub>"])
            self.shear_output.append(["V<sub>s,2-vert legs</sub> =", f"{self.beamsection.s_Vs_2_legs/1000.0:.3f}/S","kips",""])
            self.shear_output.append(["V<sub>s,4-vert legs</sub> =", f"{self.beamsection.s_Vs_4_legs/1000.0:.3f}/S","kips",""])
            self.shear_output.append(["V<sub>s,6-vert legs</sub> =", f"{self.beamsection.s_Vs_6_legs/1000.0:.3f}/S","kips",""])
        
        self.phivc_kips = round(self.vc_kips*phiv,3)
        self.vc_web = f"&#934;<sub>v</sub>V<sub>c</sub> = {self.phivc_kips} kips"
        self.vn_max_web = f"&#934;<sub>v</sub>V<sub>n,max</sub> = {self.vn_max} kips"
        
        
        # Compile Geometric Results for Web:
        self.icr_web=f"I<sub>cr</sub> ={self.icracked:.3f} in<sup>4</sup>"
        self.wt_web = f"sw = {self.beamsection.weight_plf:.3f} plf"
        self.geometry_output.append(["I<sub>g</sub> =", round(self.beamsection.Ig_in4,3),"in<sup>4</sup>","Gross Moment of Intertia neglecting Reinf."])
        self.geometry_output.append(["I<sub>cr</sub> =",round(self.icracked,3),"in<sup>4</sup>","Cracked Moment of Inertia"])
        self.geometry_output.append(["Ec =",round(self.beamsection.Ec_psi,3),"psi","Concrete Modulus of Elasticity"])
        self.geometry_output.append(["Es =",round(Es_psi/1000.0,3),"ksi","Steel Modulus of Elasticity"])
        self.geometry_output.append(["A =",round(self.beamsection.Ag_in2,3),"in<sup>2</sup>","Cross Section Area"])
        self.geometry_output.append(["Weight =",round(self.beamsection.weight_plf,3),"plf","Cross Section self weight per ft"])
        self.geometry_output.append(["Min. # of Outer Bars =",self.min_outer_bars,"",""])
        self.geometry_output.append(["Max. # of Bars per bottom layer =",self.max_bottom_bars_per_Layer,"",""])
        self.geometry_output.append(["Max. # of Bars per top layer =",self.max_top_bars_per_Layer,"",""])
        
        # Compile Torsion Results for Web:
        self.torsion_output.append(["&#934;<sub>t</sub> =",phit,"","Torsion Strength Reduction Factor"])
        self.torsion_output.append(["A<sub>cp</sub> =",Acp,"in<sup>2</sup>","Area enclosed by outside perimeter of concrete cross section"])
        self.torsion_output.append(["P<sub>cp</sub> =",Pcp,"in","Outside perimeter of concrete cross section"])
        self.torsion_output.append(["T<sub>th</sub> =", round(t_threshold/(12*1000.0),3),"ft-kips","Threshold Torsional Moment"])
        self.torsion_output.append(["&#934;<sub>t</sub>T<sub>th</sub> =", round(phit_threshold/(12*1000.0),3),"ft-kips","Ultimate Threshold Torsional Moment"])
        self.torsion_aop_status = aop_status
        
        self.phitth_web = f"&#934;<sub>t</sub>T<sub>th</sub> = {phit_threshold/(12*1000.0):.3f} ft-kips"

def pt_profile(form):
    
    web_output = []
    
    t_slab = float(form.t_slab.data)
    density = float(form.density.data)
    percent_balance = float(form.percent_balance.data)
    pt_point_left = float(form.pt_point_left.data)
    pt_point_right = float(form.pt_point_right.data)
    span = float(form.span.data)
    width = float(form.width.data)
    fpu = float(form.fpu.data)
    pt_loss = float(form.loss_psi.data)
    aps = float(form.tendon_area.data)
    tendons = float(form.num_tendon.data)
    fse = ((0.7*fpu)-pt_loss)
    pt_force = fse*aps*tendons
    
    web_output.append(["f<sub>se</sub> = ",F"(0.7*f<sub>pu</sub>-Loss), 0.7*f<sub>pu</sub> [ACI 318-14 Table 20.3.2.5.1]"])
    web_output.append(["",F"0.7*{fpu:.2f} ksi - {pt_loss:.2f} ksi"])
    web_output.append(["",F"{fse:.2f} ksi"])
    
    web_output.append(["P = ",F"f<sub>se</sub>*A<sub>ps</sub>*Number of Tendons"])
    web_output.append(["",F"{fse:.2f} ksi*{aps:.3f} in<sup>2</sup>*{tendons:.2f}"])
    web_output.append(["",F"{pt_force:.2f} kips"])
    
    A_in2 = t_slab*(width*12)
    p_over_a = (pt_force*1000)/A_in2
    p_150 = 150*A_in2 / 1000
    p_325 = 325*A_in2 / 1000
    
    self_weight = (t_slab/12.0)*density
    web_output.append(["Slab Self Weight = ",F"t<sub>slab</sub>*(1 ft / 12 in)*&rho;"])
    web_output.append(["",F"{t_slab:.2f} in*(1 ft / 12 in)*{density:.2f} pcf"])
    web_output.append(["",F"{self_weight:.2f} psf * (1 ksf / 1000 psf) = {self_weight/1000:.2f} ksf"])
    
    balance_load = (self_weight/1000.0)*width*(percent_balance/100.0)
    web_output.append(["Load to Balance =",F"Slab Self Weight * Span Width * Balance Percentage / 100.0"])
    web_output.append(["",F"{self_weight/1000:.2f} ksf * {width:.2f} ft * {percent_balance:.2f} / 100.0"])
    web_output.append(["",F"{balance_load:.2f} klf"])
    
    pt_left_top = t_slab - pt_point_left
    web_output.append(["e'<sub>left</sub> =",F"t<sub>slab</sub> - e<sub>left</sub>"])
    web_output.append(["",F"{t_slab:.2f} in - {pt_point_left:.2f} in"])
    web_output.append(["",F"{pt_left_top:.2f} in"])
    
    pt_right_top = t_slab - pt_point_right
    web_output.append(["e'<sub>right</sub> = ",F"t<sub>slab</sub> - e<sub>right</sub>"])
    web_output.append(["",F"{t_slab:.2f} in - {pt_point_right:.2f} in"])
    web_output.append(["",F"{pt_right_top:.2f} in"])
    
    e_prime_ft = (balance_load*span*span)/(8*pt_force)
    e_prime_in = 12*e_prime_ft
    
    web_output.append(["e<sup>'</sup> = ",F"( Load to Balance * Span<sup>2</sup> ) / ( 8 * PT Force)"])
    web_output.append(["",F"( {balance_load:.2f} klf * {span:.2f} ft<sup>2</sup> ) / ( 8 * {pt_force:.2f} kips)"])
    web_output.append(["",F"{e_prime_ft:.2f} ft * (12 in/ 1 ft) = {e_prime_in:.2f} in"])
    
    profile_mid = t_slab-e_prime_in-((pt_left_top+pt_right_top)/2.0)
    
    web_output.append(["e<sub>mid</sub> =",F"t<sub>slab</sub> - e<sup>'</sup> - ( e'<sub>left</sub> + e'<sub>right</sub>) / 2"])
    web_output.append(["",F"{t_slab:.2f} in - {e_prime_in:.2f} in - ( {pt_left_top:.2f} in + {pt_right_top:.2f} in) / 2"])
    web_output.append(["",F"{profile_mid:.3f} in"])
    
    p_for_e_1in = (balance_load*span*span)/(8*((t_slab-1-((pt_left_top+pt_right_top)/2.0))/12))
    
    web_output.insert(0,[F"PT Force for e<sub>mid</sub> of 1 in = {p_for_e_1in:.3f} kips or {p_for_e_1in/(fse*aps):.2f} Tendons",0])
    web_output.insert(0,[F"PT Force for 325 psi = {p_325:.3f} kips or {p_325/(fse*aps):.2f} Tendons",0])
    web_output.insert(0,[F"PT Force for 150 psi = {p_150:.3f} kips or {p_150/(fse*aps):.2f} Tendons",0])
    web_output.insert(0,[F"<b>P = {pt_force:.3f} kips</b>",0])
    
    if p_over_a < 125:
        web_output.insert(0,[F"<b>P/A = {p_over_a:.3f} psi ** Less than Min of 125 psi per ACI 318 **</b>",1])
    elif p_over_a > 325:
        web_output.insert(0,[F"<b>P/A = {p_over_a:.3f} psi (Greater than recommended Limit of 325 psi)</b>",2])
    elif p_over_a < 150:
        web_output.insert(0,[F"<b>P/A = {p_over_a:.3f} psi (Less than recommended 150 psi)</b>",2])
    else:
        web_output.insert(0,[F"<b>P/A = {p_over_a:.3f} psi </b>",0])
    
    if profile_mid < 0:
        web_output.insert(0,[F"<b>e<sub>mid</sub> = {profile_mid:.3f} in ** OUTSIDE SLAB ** </b>",1])
    elif profile_mid<1:
        web_output.insert(0,[F"<b>e<sub>mid</sub> = {profile_mid:.3f} in ** BELOW MINIMUM COVER OF 1 IN **</b>",1])
    else:
        web_output.insert(0,[F"<b>e<sub>mid</sub> = {profile_mid:.3f} in </b>",0])
    
    return web_output

def aci_unit_width_section(form):
    
    as_min_check = form.as_min_consider.data
    f_c_psi = float(form.f_prime_c_psi.data)
    cover = float(form.cover_in.data)
    cover_to = form.cover_to_select.data
    h_in = float(form.h_in.data)
    mu_ftkip = float(form.mu_ftkip.data)
    vu_kip = float(form.vu_kip.data)
    agg_size = float(form.agg_size.data)
    spacing_module = float(form.spacing_module.data)
    
    warnings = []
    
    # Check Sign on Moment
    if mu_ftkip <0:
        mu_ftkip = mu_ftkip*-1
        warnings.append("Moment was made positive for calculations, assumes cover was defined such that H-Cover is the distance to the Compression face.")
    else:
        pass
    
    if vu_kip <0:
        vu_kip = vu_kip*-1
        warnings.append("Shear was made positive for calculations.")
    else:
        pass
    
    fy_psi = 60000.0
    b_in = 12.0
    
    rebar = cbc.reinforcement(fy_psi/1000.0)
    
    web_output = []
    web_output_detailed = []
    
    #compute beta1
    beta1 = cbc.aci_beta1(f_c_psi)
    
    # Loop over each bar size to output a table of spacings
    for key, value in rebar.bar.items():
    
        bar = key
        dia = value[0]
        as_bar = value[1]
        
        if bar == 0:
            pass
        else:
            row_detailed = [f"#{bar}"]
            row_detailed.append(f"{dia:.3f}")
            row_detailed.append(f"{as_bar:.3f}")
            row_detailed.append(f"{beta1:.3f}")
            
            row = [f"#{bar}"]
            # Determine d
            if cover_to == "Bar Centroid":
                d_in = h_in - cover
                cc = cover-(dia/2.0)
                
            else:
                d_in = h_in - cover - dia/2.0
                cc = cover
            
            row_detailed.append(f"{d_in:.3f}")
            row_detailed.append(f"{cc:.3f}")
            
            # fs for computation of minimum bar spacing
            # take as 2/3 of Fy as permitted by ACI 318
            fs = (2/3.0)*fy_psi
            row_detailed.append(f"{fs/1000.0:.2f}")
            
            # General Temperature and Shrinkage Reinf. Spacing
            ts_spacing = min(5*h_in,18.0)
            
            row_detailed.append(f"{ts_spacing:.3f}")
            
            # Determin absolute min. spacing
            # ACI 318-14 25.2.1
            abs_min_spacing = max(1,dia,(4*agg_size)/3)
            row_detailed.append(f"{abs_min_spacing:.3f}")
            
            # Determine Code As,mins and min_spacing requirements
            if as_min_check == "Beam":
                
                as_min_beam = max((200*b_in*d_in),(3*math.sqrt(f_c_psi)*b_in*d_in))/fy_psi
                as_ts = max(0.0014,(0.0018*60000)/fy_psi)*b_in*h_in
                
                min_spacing = min((15*(40000/fs)) - (2.5*cc),12*(40000/fs))
                
                if as_ts >= (4*as_min_beam)/3.0:
                    as_min = as_ts
                    row_detailed.append(f"<div>{as_min:.3f}</div><div>(T&S > (4/3) As,min)</div>")
                else:
                    as_min = as_min_beam
                    row_detailed.append(f"{as_min:.3f}")
                
                row_detailed.append(f"<div>{min_spacing:.3f}</div><div>(Table 24.3.2)</div>")
                
            elif as_min_check == "One-Way Slab":
                
                # ACI 318-14 -- Table 7.6.1.1 for One-Way Slabs
                as_min = as_ts = max(0.0014,(0.0018*60000)/fy_psi)*b_in*h_in
                
                min_spacing = min((15*(40000/fs)) - (2.5*cc),12*(40000/fs))
                
                row_detailed.append(f"<div>{as_min:.3f}</div><div>(Table 7.6.1.1)</div>")
                row_detailed.append(f"<div>{min_spacing:.3f}</div><div>(Table 24.3.2)</div>")
                
            elif as_min_check == "Two-Way Slab":
                
                # ACI 318-14 -- Table 8.6.1.1 for Two-Ways slabs
                as_min = as_ts = max(0.0014,(0.0018*60000)/fy_psi)*b_in*h_in
                min_spacing = ts_spacing
                
                row_detailed.append(f"<div>{as_min:.3f}</div><div>(Table 8.6.1.1)</div>")
                row_detailed.append(f"{min_spacing:.3f}")
            else:
            # last option is Walls
            
                min_spacing = min(3*h_in,18.0)
                
                #ACI 318-14 -- Table 11.6.1
                if bar <= 5:
                    as_min = 0.0012*b_in*h_in
                
                else:
                    as_min = 0.0015*b_in*h_in
                
                row_detailed.append(f"<div>{as_min:.3f}</div><div>(Table 11.6.1)</div>")
                row_detailed.append(f"{min_spacing:.3f}")
            
            # Determine As,req for Strength
            as_strength = solve_as(fy_psi,f_c_psi,b_in,d_in,mu_ftkip)
            as_tension_control = (51*beta1*f_c_psi*b_in*d_in)/(140*fy_psi)
            
            row_detailed.append(f"{as_strength:.3f}")
            
            # Determine As, req considering minimums
            if as_min_check == "Beam":
                if as_strength >= (4*as_min_beam)/3.0:
                    as_req = as_strength
                else:
                    as_req = max(as_strength,as_min)
            else:
                as_req = max(as_strength,as_min)
            
            row_detailed.append(f"{as_req:.3f}")
            # Determine Spacing from as_req
            spacing_as = b_in / (as_req/as_bar)
            
            row_detailed.append(f"{spacing_as:.3f}")
            # Spacing to use
            spacing_use = min(spacing_as,ts_spacing,min_spacing)
            
            # Set spacing to the user defined module
            if spacing_module != 0 and spacing_use>=spacing_module:
                spacing_use = spacing_module * math.floor(spacing_use/spacing_module)
            
            row.append(f"{spacing_use:.3f}")
            row_detailed.append(f"{spacing_use:.3f}")
            # Bar Area use
            as_use = (b_in/spacing_use)*as_bar
            
            row.append(f"{as_use:.3f}")
            row_detailed.append(f"{as_use:.3f}")
            
            # Determine a
            a = (as_use*fy_psi)/(0.85*f_c_psi*b_in)
            
            row_detailed.append(f"{a:.3f}")
            
            # Compute Steel Strain
            et = (((a/beta1)-d_in)/(a/beta1))*0.003
            
            row_detailed.append(f"{et*1000.0:.3f}")
            
            # Determine phi,bending
            ety = 0.002
            factor_class = cbc.aci_phi(-1*et,ety,"Other")
            
            phi = factor_class[0]
            
            row.append(f"{phi:.3f}")
            row_detailed.append(f"{phi:.3f}")
            
            if spacing_use<spacing_module:
                row_detailed.append(f"{spacing_use:.3f} in < {spacing_module} in module")
            else:
                if spacing_use>=abs_min_spacing:
                    row_detailed.append(f"{factor_class[1]}")
                else:
                    row_detailed.append(f"Spacing Req.'d < Min.")
            
            # Only output results for bar sets with phi = 0.9
            # to the primary results
            if phi==0.9 and (spacing_use>=abs_min_spacing and spacing_use>=spacing_module):
                # Compute Mn
                mn_ftkips = (as_use*fy_psi)*(d_in - (a/2.0))*(1/(12*1000))
                phi_mn_ftkips = mn_ftkips*0.9
                
                phi_v = 0.75
                
                vc = (2*min(math.sqrt(f_c_psi),100.0)*b_in*d_in)/1000
                phi_v_vc = vc*phi_v
                
                if (phi_mn_ftkips>=(mu_ftkip-1E-6)):
                    row.append(f"{mn_ftkips:.3f}")
                    row.append(f"{phi_mn_ftkips:.3f}")
                    row.append(f"{phi_v:.3f}")
                    row.append(f"{vc:.3f}")
                    row.append(f"{phi_v_vc:.3f}")
                
                    if (vc >= vu_kip/phi_v):
                        
                        check = "OK"
                    
                    else:
                        
                        check = "V<sub>c</sub>< V<sub>u</sub>/&#934;<sub>v</sub>"
                    
                    row.append(check)
                
                web_output.append(row)
                
            web_output_detailed.append(row_detailed)
            
    return web_output, web_output_detailed, warnings
    
def solve_as(fy_psi,f_c_psi,b_in,d_in,mu_ftkip):
    # Solve the quadratic equation for As
    
    # Coefficients
    A = (fy_psi*fy_psi)/(1.7*f_c_psi*b_in)
    B = -1*fy_psi*d_in
    C = (mu_ftkip*12.0*1000.0)/0.9
    
    # Check for a (-) in the sqrt or A=0:
    if ((B*B) - (4*A*C)<0) or A==0:
        as_req=1000.0
    else:
        # Quadratic formula
        as_req = ((-1*B)-math.sqrt((B*B) - (4*A*C)))/(2*A)
    
    return as_req


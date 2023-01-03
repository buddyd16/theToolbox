# Functions and Classes for NDS 2018

import math


def lumber_density(G, mc):
    '''
    Lumber Density
    Reference: NDS 2018 - Supplement - Section 3.1.3

    Parameters:
    -----------
    G -- specific gravity : (float)
    mc -- Moisture Content % : (float)

    Returns:
    --------
    Lumber Density in lbs/ft^3 : (float)

    '''

    return 62.4*(G/(1+(G*(0.009)*(mc))))*(1+(mc/100))


def nominal_to_sds(nominalb, nominald):
    '''
    Nominal to Standard Dressed Size (sds)
    Reference: NDS 2018 - Supplement - Table 1B

    Parameters:
    -----------
    nominalb -- nominal width in inches : (float)
    nominald -- nominal depth in inches : (float)

    Returns:
    --------
    Standard Dressed Size : (dict)

    '''
    if nominalb <= 4:
        if nominalb == 1:
            sdsb = nominalb - 0.25
        else:
            sdsb = nominalb - 0.5
        
        if nominald <= 6:
            sdsd = nominald - 0.5
        else:
            sdsd = nominald - 0.75
    else:
        sdsb = nominalb - 0.5
        sdsd = nominald - 0.5
    
    return {"sdsb": sdsb, "sdsd": sdsd}


def tbl_4a_factors(nomwidth,
                    nomdepth,
                    grade,
                    repeat,
                    flatuse,
                    moisture_content,
                    fb,
                    fc):
    '''

    NDS 2018 - Supplement - Table 4A Adjustment Factors

    Parameters:
    -----------
    nomwidth -- nominal width in inches : (float)
    nomdepth -- nominal depth in inches : (float)
    grade -- commercial grade : (string)
    repeat -- Repetitive Member : (bool)
    flatuse -- member used in flatues : (bool)
    moisture_content -- moisture content : (float)
    fb -- Reference Bending stress : (float)
    fc -- Reference Compression parallel to grain stress : (float)

    Returns:
    --------
    Dictionary of factors : (dict)

    '''
    # Size Factor, Cf
    if grade == "utility":
        if nomdepth == 4:
            cf_fb = 1.0
            cf_ft = 1.0
            cf_fc = 1.0
        else:
            cf_fb = 0.4
            cf_ft = 0.4
            cf_fc = 0.6
    elif grade == "construction" or grade == "standard":
        cf_fb = 1.0
        cf_ft = 1.0
        cf_fc = 1.0
    elif grade == "stud" and nomdepth <= 6:
        if nomdepth <= 4:
            cf_fb = 1.1
            cf_ft = 1.1
            cf_fc = 1.05
        elif nomdepth <= 6:
            cf_fb = 1.0
            cf_ft = 1.0
            cf_fc = 1.0
    else:
        if nomdepth <= 4:
            cf_fb = 1.5
            cf_ft = 1.5
            cf_fc = 1.15
        elif nomdepth == 5:
            cf_fb = 1.4
            cf_ft = 1.4
            cf_fc = 1.1
        elif nomdepth == 6:
            cf_fb = 1.3
            cf_ft = 1.3
            cf_fc = 1.1
        elif nomdepth == 8:
            if nomwidth == 4:
                cf_fb = 1.3
            else:
                cf_fb = 1.2
            cf_ft = 1.2
            cf_fc = 1.05
        elif nomdepth == 10:
            if nomwidth == 4:
                cf_fb = 1.2
            else:
                cf_fb = 1.1
            cf_ft = 1.1
            cf_fc = 1.0
        elif nomdepth == 12:
            if nomwidth == 4:
                cf_fb = 1.1
            else:
                cf_fb = 1.0
            cf_ft = 1.0
            cf_fc = 1.0
        else:
            if nomwidth == 4:
                cf_fb = 1.0
            else:
                cf_fb = 0.9
            cf_ft = 0.9
            cf_fc = 0.9

    cf = {"Cf_fb": cf_fb,
            "Cf_ft": cf_ft,
            "Cf_fc": cf_fc}

    # Repetitive Member Factor, Cr
    if repeat:
        cr = 1.15
    else:
        cr = 1.0

    # Wet Service Factor, Cm
    if moisture_content <= 19:
        cm_fb = 1.0
        cm_ft = 1.0
        cm_fv = 1.0
        cm_fcp = 1.0
        cm_fc = 1.0
        cm_E = 1.0
        cm_Emin = 1.0
    else:
        if fb*cf.get("Cf_fb", 100) <= 1150:
            cm_fb = 1.0
        else:
            cm_fb = 0.85
        cm_ft = 1.0
        cm_fv = 0.97
        cm_fcp = 0.67

        if fc*cf.get("Cf_fc", 100) <= 750:
            cm_fc = 1.0
        else:
            cm_fc = 0.8

        cm_E = 0.9
        cm_Emin = 0.9

    cm = {"Cm_fb": cm_fb,
            "Cm_ft": cm_ft,
            "Cm_fv": cm_fv,
            "Cm_fcp": cm_fcp,
            "Cm_fc": cm_fc,
            "Cm_E": cm_E,
            "Cm_Emin": cm_Emin}

    # Flat Use Factor, Cfu
    if flatuse:
        if nomdepth <=3:
            cfu = 1.0
        elif nomdepth == 4:
            if nomwidth == 4:
                cfu = 1.0
            else:
                cfu = 1.1
        elif nomdepth == 5:
            if nomwidth == 4:
                cfu = 1.05
            else:
                cfu = 1.1
        elif nomdepth == 6:
            if nomwidth == 4:
                cfu = 1.05
            else:
                cfu = 1.15
        elif nomdepth == 8:
            if nomwidth == 4:
                cfu = 1.05
            else:
                cfu = 1.15
        else:
            if nomwidth == 4:
                cfu = 1.1
            else:
                cfu = 1.2
    else:
        cfu = 1.0

    adjustment_factors = {"Cf": cf,
                            "Cm": cm,
                            "Cr": cr,
                            "Cfu": cfu}

    return adjustment_factors


def tbl_4b_factors(nomwidth,
                    nomdepth,
                    species,
                    repeat,
                    flatuse,
                    moisture_content,
                    fb,
                    fc):
    '''
    
    NDS 2018 - Supplement - Table 4B Adjustment Factors

    Parameters:
    -----------
    nomwidth -- nominal width in inches : (float)
    nomdepth -- nominal depth in inches : (float)
    grade -- commercial grade : (string)
    repeat -- Repetitive Member : (bool)
    flatuse -- member used in flatues : (bool)
    moisture_content -- moisture content : (float)
    fb -- Reference Bending stress : (float)
    fc -- Reference Compression parallel to grain stress : (float)

    Returns:
    --------
    Dictionary of factors : (dict)

    '''
    # Size Factor, Cf
    if species == "Southern Pine" or species == "Mixed Southern Pine":
        if nomwidth == 4 and 8 <= nomdepth and nomdepth < 12:
            cf_fb = 1.1
            cf_ft = 1.0
            cf_fc = 1.0
        elif nomdepth >= 12:
            cf_fb = 0.9
            cf_ft = 0.9
            cf_fc = 0.9
        else:
            cf_fb = 1.0
            cf_ft = 1.0
            cf_fc = 1.0
    else:
        if nomdepth > 12:
            cf_fb = math.pow((12/nomdepth),1/9.0)
            cf_ft = 1.0
            cf_fc = 1.0
        else:
            cf_fb = 1.0
            cf_ft = 1.0
            cf_fc = 1.0

    cf = {"Cf_fb": cf_fb,
            "Cf_ft": cf_ft,
            "Cf_fc": cf_fc}

    # Repetitive Member Factor, Cr
    if repeat:
        cr = 1.15
    else:
        cr = 1.0
    
    # Flat Use Factor, Cfu
    if flatuse:
        if nomdepth <= 3:
            cfu = 1.0
        elif nomdepth == 4:
            if nomwidth == 4:
                cfu = 1.0
            else:
                cfu = 1.1
        elif nomdepth == 5:
            if nomwidth == 4:
                cfu = 1.05
            else:
                cfu = 1.1
        elif nomdepth == 6:
            if nomwidth == 4:
                cfu = 1.05
            else:
                cfu = 1.15
        elif nomdepth == 8:
            if nomwidth == 4:
                cfu = 1.05
            else:
                cfu = 1.15
        else:
            if nomwidth == 4:
                cfu = 1.1
            else:
                cfu = 1.2
    else:
        cfu = 1.0
    
    # Wet Service Factor, Cm
    if moisture_content <= 19:
        cm_fb = 1.0
        cm_ft = 1.0
        cm_fv = 1.0
        cm_fcp = 1.0
        cm_fc = 1.0
        cm_E = 1.0
        cm_Emin = 1.0
    else:
        if species == "Southern Pine - Surfaced Green":
            cm_fb = 1.0
            cm_ft = 1.0
            cm_fv = 1.0
            cm_fcp = 1.0
            cm_fc = 1.0
            cm_E = 1.0
            cm_Emin = 1.0
        
        elif species == "Southern Pine - Surfaced Dry":
            # Use Surfaced Green Values
            # Instead of finding the Surface Green Values
            # apply a Cm factor equiv. to the ratio of the reference values
            if fb == 2600:
                cm_fb = 2100/2600
                cm_ft = 1400/1750
                cm_fv = 165/175
                cm_fcp = 440/660
                cm_fc = 1300/2000
                cm_E = 1600000/1800000
                cm_Emin = 580000/660000
            elif fb == 2200:
                cm_fb = 1750/2200
                cm_ft = 1200/1450
                cm_fv = 165/175
                cm_fcp = 440/660
                cm_fc = 1100/1650
                cm_E = 1600000/1800000
                cm_Emin = 580000/660000
            else:
                cm_fb = 1600/2000
                cm_ft = 1050/1300
                cm_fv = 165/175
                cm_fcp = 440/660
                cm_fc = 1000/1500
                cm_E = 1600000/1800000
                cm_Emin = 580000/660000
        else:
            if fb*cf.get("Cf_fb", 100) <= 1150:
                cm_fb = 1.0
            else:
                cm_fb = 0.85
            cm_ft = 1.0
            cm_fv = 0.97
            cm_fcp = 0.67
            if fc <= 750:
                cm_fc = 1.0
            else:
                cm_fc = 0.8
            cm_E = 0.9
            cm_Emin = 0.9

    cm = {"Cm_fb": cm_fb,
            "Cm_ft": cm_ft,
            "Cm_fv": cm_fv,
            "Cm_fcp": cm_fcp,
            "Cm_fc": cm_fc,
            "Cm_E": cm_E,
            "Cm_Emin": cm_Emin}

    adjustment_factors = {"Cf": cf,
                            "Cm": cm,
                            "Cr": cr,
                            "Cfu": cfu}

    return adjustment_factors


def temperature_factor_ct(temp, mc):
    '''

    Compute the Temperature Factor, Ct
    Reference: NDS 2018 section 2.3.3 and Table 2.3.3

    Parameters:
    -----------
    temp -- Temperature in degrees F : (float)
    mc -- moisture content % : (float)

    Returns:
    --------
    Ct : (dict)

    '''

    if temp > 150:
        ct_E = 0.01
        ct_Emin = 0.01
        ct_ft = 0.01
        ct_fb = 0.01
        ct_fc = 0.01
        ct_fcp = 0.01
        ct_fv = 0.01
    elif temp <= 100:
        ct_E = 1.0
        ct_Emin = 1.0
        ct_ft = 1.0
        ct_fb = 1.0
        ct_fc = 1.0
        ct_fcp = 1.0
        ct_fv = 1.0
    elif temp <= 125:
        ct_E = 0.9
        ct_Emin = 0.9
        ct_ft = 0.9
        if mc > 19:           
            ct_fb = 0.7
            ct_fc = 0.7
            ct_fcp = 0.7
            ct_fv = 0.7
        else:
            ct_fb = 0.8
            ct_fc = 0.8
            ct_fcp = 0.8
            ct_fv = 0.8
    else:
        ct_E = 0.9
        ct_Emin = 0.9
        ct_ft = 0.9
        if mc > 19:           
            ct_fb = 0.5
            ct_fc = 0.5
            ct_fcp = 0.5
            ct_fv = 0.5
        else:
            ct_fb = 0.7
            ct_fc = 0.7
            ct_fcp = 0.7
            ct_fv = 0.7
        
    ct = {"Ct_fb": ct_fb,
            "Ct_fc": ct_fc,
            "Ct_fcp": ct_fcp,
            "Ct_fv": ct_fv,
            "Ct_ft": ct_ft,
            "Ct_E": ct_E,
            "Ct_Emin": ct_Emin}
    
    return ct


def incising_factor_ci(incised=True):
    '''

    Compute the Incising Factor, Ci
    Reference: NDS 2018 section 4.3.8

    Parameters:
    -----------
    incised : (bool)

    Returns:
    --------
    Ci : (dict)

    '''
    if incised:
        ci = {"Ci_E": 0.95,
                "Ci_Emin": 0.95,
                "Ci_fb": 0.80,
                "Ci_ft": 0.80,
                "Ci_fc": 0.80,
                "Ci_fv": 0.80,
                "Ci_fcp": 1.0}
    else:
        ci = {"Ci_E": 1.0,
                "Ci_Emin": 1.0,
                "Ci_fb": 1.0,
                "Ci_ft": 1.0,
                "Ci_fc": 1.0,
                "Ci_fv": 1.0,
                "Ci_fcp": 1.0}
    
    return ci


def bearing_area_factor_cb(Lb, dist_to_end):
    '''

    Compute the Bearing Area Factor, Cb
    Reference: NDS 2018 section 3.10.4

    Parameters:
    -----------
    Lb -- bearing length measured parallel to grain, in. : (float)
    dist_to_end -- distance from point of bearing to end of member, in. : (float)

    Returns:
    --------
    Cb : (dict)

    '''

    if Lb < 6 and dist_to_end >= 3:
        cb = (Lb + 0.375)/Lb
    else:
        cb = 1.0
    
    return cb


class wood_stud_wall:
    def __init__(self, geometry, stud, plate, environment, loadbracing):
        
        self.geometry = geometry
        self.stud = stud
        self.plate = plate
        self.environment = environment
        self.loadbracing = loadbracing

        #initialize Logs
        self.errors = []
        self.warning = []
        self.assumptions = []

        # Basic Geometry
        self.bnom = self.geometry.get("b", 1)
        self.dnom = self.geometry.get("d", 1)
        self.plys = self.geometry.get("plys",1)

        self.sdsdims = nominal_to_sds(self.bnom, self.dnom)
        self.bdes = self.sdsdims.get("sdsb", 1)*self.plys
        self.ddes = self.sdsdims.get("sdsd", 1)
        
        #Stud Section Properties
        self.I_in4 = (self.bdes * self.ddes**3)/12.0
        self.area_in2 = self.bdes * self.ddes
        self.s_in3 = (self.bdes * self.ddes**2)/6.0

        self.spacing_in = self.geometry.get("spacing", 24)

        # Compute wall height either inclusive or exclusive of wall plates
        self.height_in = self.geometry.get("height", 1) * 12.0
        
        if self.geometry.get("subtract plates",0) == 0:
            self.height_in = self.height_in
            self.assumptions.append('Design Stud Height = Wall Height inclusive of top and bottom plates')
        else:
            num_plates = self.geometry.get("number of plates", 0)
            self.height_in = self.height_in - (num_plates * 1.5)
            self.assumptions.append(f'Design Stud Height = Wall Height - ({num_plates})*1.5 in. wall plates')

        # Stud Bracing
        self.sheathing = self.loadbracing.get("sheathing", 1)
        self.no_sheathing = True if self.sheathing == 4 else False
        self.blocking_in = self.loadbracing.get("blocking spacing", 48)
        self.compression_face = True if self.sheathing <= 2 else False

        # Stud Design Properties
        self.fb_psi = self.stud.get("Fb", 1)
        self.fv_psi = self.stud.get("Fv", 1)
        self.fc_psi = self.stud.get("Fc", 1)
        self.Emin_psi = self.stud.get("Emin", 1)
        self.E_psi = self.stud.get("E", 1)

        # Wall Plate  - Fc,perp
        # Needed to check stud bearing 
        self.fcp_pl_psi = self.plate.get("Fcp", 1)
        
        # Compute Stud Adjustment Factors
        # Factors computed from Table 4A or 4B of the NDS 2018 Supplement
        mc = self.environment.get("moisture content", 0)

        if self.spacing_in <= 24:
            self.repeat = True
        else:
            self.repeat = False

        ndstable = self.stud.get("ndstable", "")

        if ndstable == "4A":

            self.stud_factors = tbl_4a_factors(self.bnom,
                                                self.dnom,
                                                self.stud.get("grade",""),
                                                self.repeat,
                                                False,
                                                mc, 
                                                self.fb_psi, 
                                                self.fc_psi)
        elif ndstable == "4B":
            self.stud_factors = tbl_4b_factors(self.bnom,
                                                self.dnom,
                                                self.stud.get("grade",""),
                                                self.repeat,
                                                False,
                                                mc, 
                                                self.fb_psi, 
                                                self.fc_psi)
        else:
            # User defined section all factors  are 1
            self.assumptions.append('User Stud Species Cf,Cm,Cr,Cfu = 1.0')

            cf = {"Cf_fb": 1,
                    "Cf_ft": 1,
                    "Cf_fc": 1}

            cm = {"Cm_fb": 1,
                    "Cm_ft": 1,
                    "Cm_fv": 1,
                    "Cm_fcp": 1,
                    "Cm_fc": 1,
                    "Cm_E": 1,
                    "Cm_Emin": 1}

            self.stud_factors = {"Cf": cf,
                                    "Cm": cm,
                                    "Cr": 1,
                                    "Cfu": 1}

        # Compute Plate Adjustment Factors
        # Factors computed from Table 4A or 4B of the NDS 2018 Supplement
        ndstable = self.plate.get("ndstable", "")

        if ndstable == "4A":

            self.plate_factors = tbl_4a_factors(self.bnom,
                                                self.dnom,
                                                self.plate.get("grade",""),
                                                self.repeat,
                                                False,
                                                mc, 
                                                self.fb_psi, 
                                                self.fc_psi)
        elif ndstable == "4B":
            self.plate_factors = tbl_4b_factors(self.bnom,
                                                self.dnom,
                                                self.plate.get("grade",""),
                                                self.repeat,
                                                False,
                                                mc, 
                                                self.fb_psi, 
                                                self.fc_psi)
        else:
            # User defined section all factors  are 1
            self.assumptions.append('User Plate Species Cf,Cm,Cr,Cfu = 1.0')

            cf = {"Cf_fb": 1,
                    "Cf_ft": 1,
                    "Cf_fc": 1}

            cm = {"Cm_fb": 1,
                    "Cm_ft": 1,
                    "Cm_fv": 1,
                    "Cm_fcp": 1,
                    "Cm_fc": 1,
                    "Cm_E": 1,
                    "Cm_Emin": 1}

            self.plate_factors = {"Cf": cf,
                                    "Cm": cm,
                                    "Cr": 1,
                                    "Cfu": 1}

        self.assumptions.append('Flat Use Factor (Cfu) - Wall studs are not loaded on the flat face')


        # Temperature Factor, Ct
        temp = self.environment.get("temperature", 0)
        self.ct = temperature_factor_ct(temp, mc)
        
        #Incising Factor, Ci
        incised = True if self.environment.get("incised", 0) == 1 else False
        self.ci = incising_factor_ci(incised)
        
        #Buckling Siffness Factor, CT
        #NDS 2018 4.3.11
        self.cT = 1.0
        self.assumptions.append('Buckling Stiffness Factor CT - Not Applicable for stud walls')
        
        #Bearing Area Factor, Cb
        self.cb_fcp = bearing_area_factor_cb(self.bdes, 4)
        self.assumptions.append('Bearing Area Factor Cb - Stud greater than 3" from bottom plate end')

        # Compute F_ primes
        self.compute_primes()

        # Standard Deflection Limits
        self.defl_180 = self.height_in/180.0
        self.defl_240 = self.height_in/240.0
        self.defl_360 = self.height_in/360.0
        self.defl_480 = self.height_in/480.0
        self.defl_600 = self.height_in/600.0

        self.compute_pressure_for_deflection_limits()


    def compute_primes(self):
        #Fv' = Fv * Cm * Ct * Ci - apply Cd in Fc and Fb functions
        self.cm_fv = self.stud_factors["Cm"].get("Cm_fv", 0.01)
        self.ct_fv = self.ct.get("Ct_fv", 1)
        self.ci_fv = self.ci.get("Ci_fv", 1)
        self.cfrt_fv = self.environment["Cfrt"].get("Cfrt_fv", 1)

        self.fv_prime_psi = self.fv_psi * self.cm_fv * self.ct_fv * self.ci_fv * self.cfrt_fv

        #Emin' = Emin * Cm * Ct * Ci * CT - NDS 2005 Table 4.3.1
        self.cm_Emin = self.stud_factors["Cm"].get("Cm_Emin", 1)
        self.ct_Emin = self.ct.get("Ct_Emin", 1)
        self.ci_Emin = self.ci.get("Ci_Emin", 1)
        self.cfrt_Emin = self.environment["Cfrt"].get("Cfrt_Emin", 1)
        self.Emin_prime_psi = self.Emin_psi * self.cm_Emin * self.ct_Emin * self.ci_Emin * self.cT * self.cfrt_Emin
 
        #E' = E * Cm * Ct * Ci - NDS 2005 Table 4.3.1
        self.cm_E = self.stud_factors["Cm"].get("Cm_E", 1)
        self.ct_E = self.ct.get("Ct_E", 1)
        self.ci_E = self.ci.get("Ci_E", 1)
        self.cfrt_E = self.environment["Cfrt"].get("Cfrt_E", 1)
        self.E_prime_psi = self.E_psi * self.cm_E * self.ct_E * self.ci_E * self.cfrt_E
        
        #Fc,perp' = Fc,perp * Cm * Ct * Ci * Cb- NDS 2005 Table 4.3.1
        self.cm_fcp = self.plate_factors["Cm"].get("Cm_fcp", 1)
        self.ct_fcp = self.ct.get("Ct_fcp", 1)
        self.ci_fcp = self.ci.get("Ci_fcp", 1)
        self.cfrt_fcp = self.environment["Cfrt"].get("Cfrt_fcp", 1)
        self.fcp_pl_prime_psi = self.fcp_pl_psi * self.cm_fcp * self.ct_fcp * self.ci_fcp * self.cb_fcp * self.cfrt_fcp

        self.crushing_limit_lbs = self.area_in2 * self.fcp_pl_prime_psi
        self.crushing_limit_lbs_no_cb = self.area_in2 * (self.fcp_pl_prime_psi/self.cb_fcp)


    def compute_pressure_for_deflection_limits(self):
        # Pressure to reach deflection limits
        # (5 w l^4 / 384 E I ) 1728 in3/ft3 = delta
        # delta 384 E I / 1728 5 l^4 = w, where w is in plf
        # w / (spacing / 12) converts to psf
        self.defl_180_w_psf = ((self.defl_180 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)
        self.defl_240_w_psf= ((self.defl_240 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)
        self.defl_360_w_psf = ((self.defl_360 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)
        self.defl_480_w_psf = ((self.defl_480 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)
        self.defl_600_w_psf = ((self.defl_600 * 384 * self.E_prime_psi * self.I_in4) / (1728 * 5 * (self.height_in/12.0)**4))/(self.spacing_in/12.0)


    def fc_prime_calc(self, cd):
        #apply cd to Fv'
        self.fv_prime_psi_cd = self.fv_prime_psi * cd
        #Fc* = reference compression design value parallel to grain multiplied by all applicable adjusment factors except Cp
        self.cm_fc = self.stud_factors["Cm"].get("Cm_fc", 1)
        self.ct_fc = self.ct.get("Ct_fc", 1)
        self.cf_fc = self.stud_factors["Cf"].get("Cf_fc", 1)
        self.ci_fc = self.ci.get("Ci_fc", 1)
        self.cfrt_fc = self.environment["Cfrt"].get("Cfrt_fc", 1)
        self.fc_star_psi = self.fc_psi * cd * self.cm_fc * self.ct_fc * self.cf_fc * self.ci_fc * self.cfrt_fc
        
        self.c_cp = 0.8
        self.assumptions_c = 'c for Cp calculation based on sawn lumber - NDS 2005 3.7.1\n'
        
        #Slenderness Ratio check per NDS 2005 sections 3.7.1.2 thru 3.7.1.4
        kb = 1.0
        kd = 1.0

        self.assumptions_ke = '\nKe = 1.0 for both depth and breadth of studs - Ref NDS 2005 appendix G pin top and bottom\n'

        if self.no_sheathing and self.blocking_in > 0:
            leb = self.blocking_in
            self.assumptions_leb = 'Le_b = {0:.2f} in. - no sheathing weak axis only braced by blocking\n Confirm load path exists for bracing force.\n'.format(leb)
        
        elif self.no_sheathing and self.blocking_in <= 0:
            leb = self.height_in
            self.assumptions_leb = 'Le_b = {0:.2f} in. - no sheathing and no blocking - weak axis unbraced.\n'.format(leb)
        
        else:
            leb = 12 * kb
            self.assumptions_leb = 'Le_b = 12.0 in. - continuously braced by sheathing 12" field nailing assumed\n'
        
        led = self.height_in * kd
        self.le_b = leb
        
        #Check Le/d,b ratios less than 50 - NDS 2005 Section 3.7.1.4
        if leb / self.bdes > 50 or led/self.ddes > 50:
            ratio_status = 0
        else:
            ratio_status = 1.0
        
        if ratio_status == 1.0:
            #FcE = 0.822 * Emin' / (Le/d)^2 - NDS 2005 Section 3.7.1
            self.fcE_psi = (0.822 * self.Emin_prime_psi)/(max(leb/self.bdes,led/self.ddes))**2
            
            #Cp = ([1 + (FcE / Fc*)] / 2c ) - sqrt[ [1 + (FcE / Fc*) / 2c]^2 - (FcE / Fc*) / c] - NDS 2005 Section 3.7.1
            self.cp = ((1+(self.fcE_psi/self.fc_star_psi))/(2*self.c_cp))-((((1+(self.fcE_psi/self.fc_star_psi))/(2*self.c_cp))**2)-((self.fcE_psi/self.fc_star_psi)/self.c_cp))**0.5
            
            self.fc_prime_psi = self.fc_star_psi * self.cp
            self.assumptions_cp = 'Wall studs are not tapered and not subject to NDS 2005 - 3.7.2\n'
        else:
            self.fc_prime_psi = 1
            self.fcE_psi = 1
            self.cp = 0.001
            self.warning.append('Slenderness ratio greater than 50, suggest increase stud size or reducing wall height')
            self.assumptions_cp = ''
    
        return self.fc_prime_psi
    
    def fb_prime_calc(self, cd):

        #apply cd to Fv'
        self.fv_prime_psi_cd = self.fv_prime_psi * cd
        
        #Beam Stability Factor, CL
        #NDS 2005 section 4.3.5
        if self.compression_face:
            self.cl = 1.0 #Assumes stud walls are sheathed on the compression face
            self.assumptions.append('Beam Stability Factor_CL - Wall studs are continuously sheathed on the compression face')
        else:
            if self.blocking_in == 0 or self.blocking_in > self.height_in:
                self.lu_bending_in = self.height_in
            else:
                self.lu_bending_in = self.blocking_in
                
            if self.height_in/self.ddes < 7.0:
                self.cl_le = 2.06 * self.lu_bending_in
            elif self.height_in/self.ddes <= 14.3:
                self.cl_le = (1.63 * self.lu_bending_in)+(3*self.ddes)
            else:
                self.cl_le = 1.84 * self.lu_bending_in   
            
            self.Rb_cl = (self.cl_le*self.ddes/self.bdes**2)**0.5
            self.Fbe_cl = (1.20 * self.Emin_prime_psi)/self.Rb_cl**2
            self.assumptions.append('Beam Stability Factor CL - Wall studs are not braced on compression face - CL per design stud/blocking height')

        self.cm_fb = self.stud_factors["Cm"].get("Cm_fb", 1)
        self.ct_fb = self.ct.get("Ct_fb", 1)
        self.cf_fb = self.stud_factors["Cf"].get("Cf_fb", 1)
        self.cfu = self.stud_factors.get("Cfu", 1)
        self.ci_fb = self.ci.get("Ci_fb", 1)
        self.cr = self.stud_factors.get("Cr", 1)
        self.cfrt_fb = self.environment["Cfrt"].get("Cfrt_fb", 1)

        if self.compression_face:
            self.fb_prime_psi = self.fb_psi * cd * self.cm_fb * self.ct_fb * self.cl * self.cf_fb * self.cfu * self.ci_fb * self.cr * self.cfrt_fb
        else:
            self.fb_star_psi = self.fb_psi * cd * self.cm_fb * self.ct_fb * self.cf_fb * self.cfu * self.ci_fb * self.cr * self.cfrt_fb
            self.fbe_fbstar = self.Fbe_cl / self.fb_star_psi
            #NDS equation 3.3-6
            self.cl = ((1+self.fbe_fbstar)/1.9) - ((((1+self.fbe_fbstar)/1.9)**2) - (self.fbe_fbstar)/0.95)**0.5
            self.fb_prime_psi = self.fb_psi * cd * self.cm_fb * self.ct_fb * self.cl * self.cf_fb * self.cfu * self.ci_fb * self.cr * self.cfrt_fb
            self.cl_calc_text = "\n\n--Calculation of CL--\nLe = {0:.3f} in - per NDS Table 3.3.3 footnote 1 \nRb = sqrt(Le*d / b^2) = {1:.3f}\nFbE = 1.20 * Emin' /Rb^2 = {2:.3f} psi\nFb* = reference bending design value multiplied by all applicable adjustment factors except Cfu, Cv, and CL\nFb* = {3:.3f} psi\nFbE/Fb* = {4:.3f}\nNDS Eq. 3.3-6\nCL = [1 + (FbE / Fb*)] / 1.9 - ( [ [1 + (FbE / Fb*)] / 1.9 ]^2 - (FbE / Fb*) / 0.95 ) ^ 1/2 = {5:.3f}".format(self.cl_le, self.Rb_cl, self.Fbe_cl, self.fb_star_psi, self.fbe_fbstar, self.cl)
            
        return self.fb_prime_psi
    
    def axial_and_bending(self, cd, p_lbs, m_inlbs):
        fc_psi = p_lbs / self.area_in2
        fb_psi = abs(m_inlbs/self.s_in3)
        
        fc_prime = self.fc_prime_calc(cd)
        fb_prime = self.fb_prime_calc(cd)
        
        #Check that fc is less than FcE per NDS 2005 - Section 3.9.2
        if fc_psi < self.fcE_psi:
            #Combine ratio per NDS 2005 equation (3.9-3)
            #[fc/Fc']^2 + fb / Fb' [ 1- (fc / FcE)] <= 1.0
            ratio = (fc_psi/fc_prime)**2 + (fb_psi / (fb_prime*(1-(fc_psi/self.fcE_psi))))
            if ratio > 1.0:
                self.warning=self.warning + 'Combined Axial and Bending ratio > 1.0\n'
                return 'NG'
            else:
                return 'OK'
        else:
            self.warning=self.warning + 'fc is greater than FcE\n'
            return 'NG'
        
    def axial_capacity_w_moment(self,cd,m_inlbs,e_in):
        #solve for the allowable axial load using the bisection method
        a=0
        b=self.area_in2 * self.fc_prime_calc(cd) #upper bound limit on axial strength
        c=0
        
        loop_max = 500
        tol = 0.00001
        loop = 0
        p_lbs = 0
        while loop<loop_max:
            c = (a+b)/2.0
            
            fc_psi = c / self.area_in2
            fb_psi = abs((m_inlbs)/self.s_in3)
          
            fc_prime = self.fc_prime_calc(cd)       
            fb_prime = self.fb_prime_calc(cd)
            
            if self.fc_prime_psi == 1 and self.fcE_psi == 1:
                p_lbs = 1
                loop = loop_max
            else:            
                #Check that fc is less than FcE per NDS 2005 - Section 3.9.2
                if fc_psi < self.fcE_psi:
                    if e_in ==0:
                        #Combine ration per NDS 2005 equation (3.9-3)
                        #[fc/Fc']^2 + fb / Fb' [ 1- (fc / FcE)] <= 1.0
                        ratio = (fc_psi/fc_prime)**2 + (fb_psi / (fb_prime*(1-(fc_psi/self.fcE_psi))))
                    else:
                        #Combined Ratio per NDS 2005 equation 15.4-1
                        #[fc/Fc']^2 + (fb + fc(6e/d)[1 + 0.234 (fc / FcE)])/ Fb' [ 1- (fc / FcE)] <= 1.0
                        ratio = (fc_psi/fc_prime)**2 + ((fb_psi+(fc_psi*(6*e_in/self.ddes)*(1+(0.234*(fc_psi/self.fcE_psi)))))/ (fb_prime*(1-(fc_psi/self.fcE_psi))))
                else:
                    ratio = 2.0
                
                if ratio > 1.0:
                    b = c
                else:
                    a = c
                
                if (b-a)/2.0 <= tol:
                    loop = loop_max
                    p_lbs = c
                else:
                    loop+=1
        
        return p_lbs
    
    def wall_interaction_diagram_cd(self, cd, e_in,s_in):
        
        if s_in == 0:
           diag_spacing_in  = self.spacing_in
        else:
           diag_spacing_in = s_in
        
        # Find bending limit pressure for each Cd ie where fb = Fb'
        # fb = M/s , M in in-lbs and s in in^3
        # M = w * stud height^2 / 8
        # w = Fb' * s * 8 / stud height^2 * (12 in / 1 ft)
        
        self.w_plf_limit = ((self.fb_prime_calc(cd) * self.s_in3 * 8.0) / (self.height_in**2)) * 12.0
        self.w_psf_limit = self.w_plf_limit/(diag_spacing_in/12.0)

        # Determine pure axial compression capacity ie where fc = Fc' - withou consideration for plate crushing
        # fc = P/a
        # P = a * Fc'
        if e_in == 0:
            self.p_lbs_limit = self.area_in2 * self.fc_prime_calc(cd)
            d=[0] #deflection at pressure x
        else:
            self.p_lbs_limit = self.axial_capacity_w_moment(cd,0, e_in)
            d=[(((self.p_lbs_limit*e_in)*self.height_in**2)/(16.0*self.E_prime_psi*self.I_in4))]
            
        points = 50
        step = self.w_psf_limit/points
        
        w=0
        x=[0] #pressure on x-axis
        y=[self.p_lbs_limit/ (diag_spacing_in /12.0)] #axial force on y-axis

        
        for i in range(1,points):
            w = step*i
            x.append(w)
            w_plf = w * (diag_spacing_in/12)
            moment_inlbs = (((w_plf) * (self.height_in/12)**2) / 8.0)*12
            
            deflection = (5 * (w_plf) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728
            
            p_lbs = self.axial_capacity_w_moment(cd,moment_inlbs, e_in)
            p_plf = p_lbs/ (diag_spacing_in /12.0)
            
            if e_in ==0:
                deflection = deflection
            else:
                deflection = deflection + (((p_lbs*e_in)*self.height_in**2)/(16.0*self.E_prime_psi*self.I_in4))
            
            d.append(deflection)
            y.append(p_plf)
        
        x.append(self.w_psf_limit)
        y.append(0)
        d.append((5 * (self.w_plf_limit) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728)
        return x,y,d
        
    def wall_pm_diagram_cd(self, cd, e_in, s_in):
        
        if s_in == 0:
           diag_spacing_in  = self.spacing_in
        else:
           diag_spacing_in = s_in
           
        # Find bending limit pressure for each Cd ie where fb = Fb'
        # fb = M/s , M in in-lbs and s in in^3
        
        self.m_inlbs_limit = (self.fb_prime_calc(cd) * self.s_in3)

        # Determine pure axial compression capacity ie where fc = Fc' - withou consideration for plate crushing
        # fc = P/a
        # P = a * Fc'
        if e_in == 0:
            self.p_lbs_limit = self.area_in2 * self.fc_prime_calc(cd)
        else:
            self.p_lbs_limit = self.axial_capacity_w_moment(cd,0, e_in)
            
        points = 50
        step = self.m_inlbs_limit/points
        
        m=0
        x=[0] #moment on x-axis
        y=[self.p_lbs_limit/ (diag_spacing_in /12.0)] #axial force on y-axis
        if e_in==0:
            d=[0] #deflection at equivalent uniform load x
        else:
            d=[(((self.p_lbs_limit*e_in)*self.height_in**2)/(16.0*self.E_prime_psi*self.I_in4))]
        
        for i in range(1,points):
            m = step*i
            moment_inlbs = m
            x.append(m)
            w_plf = ((((m/12.0) * 8.0) / ((self.height_in/12.0)**2)))
            deflection = (5 * (w_plf) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728
            p_lbs = self.axial_capacity_w_moment(cd,moment_inlbs, e_in)
            p_plf = p_lbs / (diag_spacing_in /12.0)
            y.append(p_plf)
            
            if e_in ==0:
                deflection = deflection
            else:
                deflection = deflection + (((p_lbs*e_in)*self.height_in**2)/(16.0*self.E_prime_psi*self.I_in4))
            d.append(deflection)
            

        
        x.append(self.m_inlbs_limit)
        y.append(0)
        w_plf = ((((self.m_inlbs_limit/12.0) * 8.0) / ((self.height_in/12.0)**2)))
        d.append((5 * (w_plf) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728)
        return x,y,d
        
    def wall_pm_diagram_cd_stud(self, cd, e_in):
           
        # Find bending limit pressure for each Cd ie where fb = Fb'
        # fb = M/s , M in in-lbs and s in in^3
        
        self.m_inlbs_limit = (self.fb_prime_calc(cd) * self.s_in3)

        # Determine pure axial compression capacity ie where fc = Fc' - withou consideration for plate crushing
        # fc = P/a
        # P = a * Fc'
        if e_in == 0:
            self.p_lbs_limit = self.area_in2 * self.fc_prime_calc(cd)
        else:
            self.p_lbs_limit = self.axial_capacity_w_moment(cd,0, e_in)
            
        points = 50
        step = self.m_inlbs_limit/points
        
        m=0
        x=[0] #moment on x-axis
        y=[self.p_lbs_limit] #axial force on y-axis
        if e_in==0:
            d=[0] #deflection at pressure x
        else:
            d=[(((self.p_lbs_limit*e_in)*self.height_in**2)/(16.0*self.E_prime_psi*self.I_in4))]
        
        for i in range(1,points):
            m = step*i
            moment_inlbs = m
            x.append(m)
            w_plf = ((((m/12.0) * 8.0) / ((self.height_in/12.0)**2)))
            deflection = (5 * (w_plf) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728
            p_lbs = self.axial_capacity_w_moment(cd,moment_inlbs, e_in)
            y.append(p_lbs)
            
            if e_in ==0:
                deflection = deflection
            else:
                deflection = deflection + (((p_lbs*e_in)*self.height_in**2)/(16.0*self.E_prime_psi*self.I_in4))
            d.append(deflection)
            
        x.append(self.m_inlbs_limit)
        y.append(0)
        w_plf = ((((self.m_inlbs_limit/12.0) * 8.0) / ((self.height_in/12.0)**2)))
        d.append((5 * (w_plf) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728)
        return x,y,d
        
    def cap_at_common_spacing(self, cd,lateral_w_psf, e_in, crush=1):
        spacings = [4,6,8,12,16,24]
        res_string = 'Axial Capacity at 4" - 6" - 8" - 12" - 16" - 24" spacings:\n'
        self.cap_at_common = []
        
        for s in spacings:
            w_plf = lateral_w_psf * (s/12.0)
            m_inlbs =  ((w_plf * (self.height_in/12.0)**2)/8.0)*12
            deflection = (5 * (w_plf) * (self.height_in/12)**4)/(384*self.E_prime_psi*self.I_in4)*1728
            
            p_lbs = self.axial_capacity_w_moment(cd,m_inlbs,e_in)
            if crush == 1:
                p_lbs = min(p_lbs,self.crushing_limit_lbs)
            else:
                p_lbs = p_lbs
                
            p_plf = p_lbs / (s/12.0)
            
            if e_in ==0:
                deflection = deflection
            else:
                deflection = deflection + (((p_lbs*e_in)*self.height_in**2)/(16.0*self.E_prime_psi*self.I_in4))
            
            d_ratio = self.height_in / deflection
            d_string = 'H/{0:.1f}'.format(d_ratio)
            
            res_string = res_string + '{0:.3f} ft - {1}" O.C. - {2:.2f} Lbs ({3:.2f} plf) - {4}\n'.format(self.height_in/12.0,s,p_lbs,p_plf,d_string)
            res_list = [s,p_lbs,p_plf,d_string]
            self.cap_at_common.append(res_list)
        
        return res_string
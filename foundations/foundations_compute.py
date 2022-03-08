'''
BSD 3-Clause License
Copyright (c) 2022, Donald N. Bockoven III
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import math


def IBC_18_1(qh,p,h,b,d):
    '''
    Inputs:
    qh: float       Allowable lateral bearing pressure 
    p: float        Applied Lateral Load
    h: float        Distance from Ground surface to point of application of P
    b: float        Diameter or Diagonal Dimension of Pier foundation
    d: float        Depth of Embedment

    Output:
    dcalc: float        Calculated Depth of Embedment per IBC 18-1
    '''

    # S1 = min(1/3 qh d, 4 qh)
    # allowable lateral soil-bearing pressure as set forth in Section 1806.2
    # based on a depth of one-third the depth of embedment in psf (kPa)
    # d definition includes
    # "but not over 12 feet for purpose of computing lateral pressure"
    s1 = min((1/3)*qh*d, 4*qh)

    # A = 2.34 P / (S1 b)
    A = (2.34*p)/(s1*b)

    # Eq 18-1 -- 0.5*A ( 1+ (1+(4.36h/A))^1/2)
    dcalc = (0.5*A)*(1+(1+((4.36*h)/A))**0.5)

    return {"d":dcalc,"s1":s1,"A":A}

def rutledge_mo(A,d,s1,b,p):
    c = 0.5*A
    f = d-A
    e = 0.5*f
    q1 = A*s1*b
    q2 = q1-p
    mo = (-1*q2*(e+A))+(q1*c)

    return {"mo":mo,"c":c,"f":f,"e":e,"q1":q1,"q2":q2}

def web_ibc_18_1(inputs):

    qh = inputs["qh"]
    allow_180634 = inputs["allow_180634"]
    p = inputs["p"]
    h = inputs["h"]
    shape = inputs["shape"]
    shape_size = inputs["shape_size"]
    dignore = inputs["dignore"]

    # IBC 1806.3.4 allows for 2x qh if 1/2" lateral displacement at the ground
    # surface can be tolerated. This is a user choice so just need to check if
    # it was selected and apply the 2x to qh.
    if allow_180634 == 1:
        qh = 2*qh
    
    # effective ground surface starts at the base of d,ignore so
    # h needs to be increased by the d,ignore depth for computation
    # note the reported embedment depth will need to be the computed value
    # plus the ignore depth.
    h = h+dignore

    # b is the diamter or diagonal distance of the pier shape
    if shape == "round":
        b = shape_size/12.0 # convert b to ft 
    else:
        # only options for shape are round or square
        # h = sqrt(x^2+y^2) for a square x=y so
        # h = sqrt(x^2+x^2) = sqrt(2*x^2)
        b = ((2*shape_size*shape_size)**0.5)/12.0 # convert b to ft 

    # comutation of d is dependant on itself, so use a root finding method
    # to solve for d. The problem is well defined so we will use the bisection 
    # method which will have an acceptable convergence rate for this problem.

    # define a tolerance for d-dcalc
    tol = 1E-6

    # also define a maximum number of iterations to kick out of the loop
    max_iters = 1000

    i = 0
    # Bisection Method
    da = 0.1
    db = 1000
    dc = 1
    dcc = {"d":100}

    while (i < max_iters and abs(dcc["d"]-dc) > tol):

        dac = IBC_18_1(qh,p,h,b,da)
        dbc = IBC_18_1(qh,p,h,b,db)

        dc = (da+db)/2
        dcc = IBC_18_1(qh,p,h,b,dc)

        if (dc - dcc["d"])< 0:
            da = dc
        else:
            db = dc
        
        i+=1

    dcc = IBC_18_1(qh,p,h,b,dc)
    results = {"b":b, "d":dcc["d"],"duse":dcc["d"]+dignore, "accuracy":abs(dcc["d"]-dc),"iterations":i}
    # effective moment at the groud surface, where the ground surface starts
    # at the base of d,ignore.
    meff = p*h
    results['meff'] = meff

    # IBC 18-1 is a modifed version of the Rutledge Nomograph formula
    # IBC does note define A, so we will assume for the purposes of 
    # presenting shear and moment on the embeded pier we will compute
    # A as presented in Figure 2 from Pole Building Design by Donald Patterson

    mo = meff 
    md = mo + (p*results["d"])
    s1 = dcc["s1"]

    results["s1"] = s1
    results["A"] = dcc["A"]

    # use the bisection method again
    aa = 0.1
    ab = results["d"]
    mdiff_c = 1

    i=0
    while (i < max_iters and abs(mdiff_c)>tol):

        rutledge_a = rutledge_mo(aa,results["d"],s1,b,p)
        rutledge_b = rutledge_mo(ab,results["d"],s1,b,p)

        ac = (aa+ab)/2.0
        rutledge_c = rutledge_mo(ac,results["d"],s1,b,p)

        mdiff_a = rutledge_a["mo"] + mo
        mdiff_b = rutledge_b["mo"] + mo
        mdiff_c = rutledge_c["mo"] + mo

        if mdiff_c < 0:
            ab = ac
        else:
            aa = ac
        
        i+=1
    
    rutledge_c = rutledge_mo(ac,results["d"],s1,b,p)
    # assuming the bisection method converged
    rutledge_c["A"] = ac
    rutledge_c["S1"] = rutledge_c["q1"]/rutledge_c["A"]
    rutledge_c["S2"] = rutledge_c["q2"]/rutledge_c["f"]

    print(ac)

    # paramtric list of stations between 0 and 1'
    eta = [0+i*(1/100) for i in range(100+1)]

    stations = [results["d"]*i for i in eta]

    voy = p / rutledge_c["S1"]

    stations.append(voy)

    stations.sort()

    # Shear
    shear = []
    v_max = [0,0]
    for k,y in enumerate(stations):
        if y < rutledge_c["A"]:
            v = p - (y*rutledge_c["S1"])
        else:
            v = p - (rutledge_c["A"]*rutledge_c["S1"]) + (rutledge_c["S2"]*(y-rutledge_c["A"]))
        
        if abs(v) >= v_max[0]:
            v_max[0] = abs(v)
            v_max[1] = stations[k]

        shear.append(v)
    
    # Moment
    moment = []
    m_max = [0,0]
    for k,y in enumerate(stations):
        if y < rutledge_c["A"]:
            m = mo+(p*y)-(0.5*rutledge_c["S1"]*y*y)
        else:
            m = (mo
            + (p*y)
            - ((rutledge_c["S1"]*rutledge_c["A"])*((rutledge_c["A"]/2)+(y-rutledge_c["A"])))
            + (0.5*rutledge_c["S2"]*math.pow(y-rutledge_c["A"],2)))

        if m >= m_max[0]:
            m_max[0] = m
            m_max[1] = stations[k]

        moment.append(m)

    plot_stations = [-1*j for j in stations]

    results["rutledge"] = rutledge_c
    results["y_stations"] = plot_stations
    results["v_plot"] = shear
    results["m_plot"] = moment
    results["m_max"] = m_max
    results["v_max"] = v_max

    return results
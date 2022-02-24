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


import analysis.geometry2D as g2d
import analysis.ebloads as ebl
import analysis.loadcombos as LC
import analysis.flexibility2D as solve2d
import analysis.beamtools as bmtools

# import geometry2D as g2d
# import ebloads as ebl
# import loadcombos as LC
# import flexibility2D as solve2d
# import beamtools as bmtools

#import matplotlib.pyplot as plt
import math


class Beam2D():
    '''
    A class representing a 2D - Euler-Bernoulli Beam
    '''

    def __init__(self, userName, node_i, node_j, Em, Ixx, endCondition=[0, 0], userid=1):

        self.userName = userName            # User defined name
        self.node_i = node_i                # Beam i node (x,y)
        self.node_j = node_j                # Beam j node (x,y)
        self.Em = Em                        # Beam modulus of elasticity
        self.Ixx = Ixx                      # Beam moment of inertia about
                                            # the axis of bending
        self.endCondition = endCondition    # Beam end condition 1-fixed 0-pin

        self.id = userid                    # The span id of this beam

        # Initiliaze empty data sets for other variable beam info
        self.interiorSupports = []  # List of additional support locations, as a 
                                    # relative distance from the i end along beam.
        self.Loads = []             # List to hold the applied loads
        self.reactions_basic = {}   # Dictionary to hold Basic reactions
        self.reactions_uls = {}     # Dictionary to hold ULS reactions
        self.reactions_sls = {}     # Dictionary to hold Service Reactions
        self.v_functions_uls = {}
        self.m_functions_uls = {}
        self.v_functions_sls = {}
        self.m_functions_sls = {}
        self.eis_functions_sls = {}
        self.eid_functions_sls = {}
        self.v_functions_basic = {}
        self.m_functions_basic = {}
        self.eis_functions_basic = {}
        self.eid_functions_basic = {}
        self.Mu_max = []            # List to hold Mu,max (ULS Moment Envelope)
        self.Mu_min = []            # List to hold Mu,min (ULS Moment Envelope)
        self.Vu_max = []            # List to hold Vu,max (ULS Shear Envelope)
        self.Vu_min = []            # List to hold Vu,min (ULS Shear Envelope)
        self.Ms_max = []            # List to hold Ms,max (Service Moment Envelope)
        self.Ms_min = []            # List to hold Ms,min (Service Moment Envelope)
        self.Vs_max = []            # List to hold Vs,max (Service Shear Envelope)
        self.Vs_min = []            # List to hold Vs,min (Service Shear Envelope)
        self.Ss_min = []             # List to hold Slope,min (Service Envelope)
        self.Ss_max = []             # List to hold Slope,max (Service Envelope)
        self.Ds_min = []             # List to hold Deflection,min (Service Envelope)
        self.Ds_max = []             # List to hold Deflection,max (Service Envelope)
        self.FEF_basic = {}
        self.FEF_sls = {}
        self.FEF_uls = {}
        
        self.calcstations = []
        self.rootstations = []
        self.printstations = []
        self.chartstations = []
        
        self.analyzed = False

    @property
    def span(self):
        '''
        Compute the length of the beam
        '''

        x1 = self.node_i.x
        y1 = self.node_i.y
        x2 = self.node_j.x
        y2 = self.node_j.y

        self._span = (((x2-x1)**2)+((y2-y1)**2))**0.5

        return self._span

    def addinteriorsupport(self, location):
        '''
        Add an interior support to the beam interiorSupports list
        '''

        self.interiorSupports.append(location)

    def addLoads(self, newLoads):
        '''
        newLoads = []  list of load classes

        Loads should already be converted to one of the load class types
        prior to adding them to the beam
        '''

        self.Loads.extend(newLoads)

    def spans(self):
        '''
        compute the list of spans making up the total beam span
        considering interior supports.

        returns a list of floats   [s1,...,si]
        '''
        
        spans = []
        
        if self.interiorSupports == []:
            spans.append(self.span)
        else:
            for i, support in enumerate(self.interiorSupports):
                
                if i == 0:
                    spans.append(support)
                else:
                    spans.append(support-self.interiorSupports[i-1])
            
            spans.append(self.span - self.interiorSupports[-1])
        
        return spans

    def computation_stations(self, num_stations=26):
        '''
        define general computation points along the beam length for shear,
        moment, slope, and deflection plots
        '''
        extra_stations = []

        # paramtric list of stations between 0 and 1'
        eta = [0+i*(1/num_stations) for i in range(num_stations+1)]

        if self.interiorSupports == []:
            stations = [self.span*i for i in eta]

        else:

            stations = []

            spans = self.spans()

            for j,span in enumerate(spans):

                if j == 0:
                    stations.extend([span*i for i in eta])
                else:
                    stations.extend([stations[-1] + span*i for i in eta])

            for support in self.interiorSupports:

                extra_stations.append(support-0.001)
                extra_stations.append(support+0.001)

        # Loop through the applied loading and generate calculation points
        # at start and ends of distributed loadings and at point loadings
        # include an additional point at a small tolerance before and after
        # each location to ensure diagram discontinuities are captured.
        Loads = self.Loads

        if Loads == []:
            pass
        else:
            for load in Loads:
                if load.kind == 'POINT' or load.kind=='MOMENT':
                    b = min(self.span, load.a + 0.001)
                    c = max(0, load.a - 0.001)
                    extra_stations.extend([c, load.a, b])

                elif load.kind == 'UDL' or load.kind=='TRAP':
                    c = min(self.span, load.b+0.001)
                    d = max(0, load.a-0.001)
                    extra_stations.extend([d, load.a, load.b, c])
                else:
                    pass

        stations.extend(extra_stations)

        stations.sort()

        # Make sure the first and last stations do not exceed the beam

        if stations[0] < 0:
            stations[0] = 0

        if stations[-1] > self.span:
            stations[-1] = self.span

        # Remove duplicate locations

        self.calcstations = sorted(set(stations))
      
    
    def flexibility_analyze(self, LoadCombos, patterns, offpatternfactors={}):
        '''
        For each of the load combinations and load patterns within each combination
        specified perform an analysis using the flexibility method to determine interior
        reactions and then go on to fill in the results lists.

        Steps are:
        1. Determine deflections at each support location for the released model
        2. Solve for the restoring point loads at the supports such that the
            deflection at the support location is 0. For end fixity the solution
            aims to results in 0 rotation at a fixed end.
        3. Save the reactions to the appropriate reaction dictionary base on the 
            load combination type.
        4. Apply the reactions as point loads/point moments. The reactions will
            only exist as loads in the scope of this function.  
        5. Loop through the calculation stations and loads to build the v,m,s,d
            diagrams. For ULS and SLS combos compare current station value to
            the max/min data lists and update to the current value if it is 
            greater than the max or less than the min.

        '''

        # Check if there are any loads if not then 
        # nothing to perform an analysis on

        if self.Loads == []:

            # no loads do nothing
            pass

        else:
            for combo in LoadCombos:

                combo_key = combo.name

                if combo.patterned and (self.id != 1 or self.interiorSupports !=[]):

                    # we only need to pattern loads if the beam is not the only beam
                    # or if there are interior supports
                    
                    if all(x==1 for x in offpatternfactors.values()):
                        # if all the off pattern factors are 1 then
                        # there is no reason to actually pattern
                        # because the beam element may not be the only span
                        # set the pattern of all 1's for each element
                        # in one of the defined patterns
                        
                        calc_patterns = [[1 for p in patterns[0]]]
                        
                    else:
                        calc_patterns = patterns
                
                else:
                    
                    # if not considering patterning then use a single calc
                    # pattern of [1,....,1] for len(spans)
                    # do this so that a.) we don't need to copy all this work
                    # for a non-pattern case b.) keep resulting dictionaries
                    # consistent such that the results exist in a pattern key
                    calc_patterns = [[ 1 for p in patterns[0]]]
                    
                rdict = {}
                fefdict = {}
                vfunc = {}
                mfunc = {}
                eisfunc = {}
                eidfunc = {}
                    
                for pattern  in calc_patterns:
                    
                    endSlopes = [0, 0]
                    intDelta = [0 for i in self.interiorSupports]
                    
                    rltemp = 0
                    rrtemp = 0
                    
                    vfunctemp = []
                    mfunctemp = []
                    eisfunctemp = []
                    eidfunctemp = []
                    feftemp = [0,0,0,0]

                    pattern_key = pattern
                    
                    for load in self.Loads:
                        

                        if load.loadtype in combo.factors or load.loadtype == f'{combo_key}{pattern_key}':
                            # Load type is part of the current combo
                            
                            if load.loadtype == f'{combo_key}{pattern_key}':
                                # if the load is a result of the current combination
                                # and pattern set the LF to 0.
                                # this will be used to set the start slopes for
                                # cantilevers
                                
                                LF = 1.0
                            
                            else:
                            
                                LF = combo.factors[load.loadtype]
                                
                                if load.loadtype in offpatternfactors:
                                    # if the load type exists in the offpattern
                                    # factor list then the load is a type that 
                                    # should be pattterned
                                    LFoffpat = offpatternfactors[load.loadtype]
    
                                    # pattern is of the form [1,...,i]
                                    # where the index is equal to the span
                                    # since the list index starts at 0
                                    # subtract 1 from the load.span property
                                    # to align with the list indexs
                                    LFpat = pattern[load.span-1]
    
                                    if LFpat == 0:
                                        LF = LF*LFoffpat
                                    else:
                                        LF = LF

                            if LF == 0:
                                # 0 load factor therefore no reason to move 
                                # forward with the current load
                                pass
                            else:
                                
                                # get slope at start and end of beam from load
                                endSlopes[0] += load.eisx(0)*LF
                                endSlopes[1] += load.eisx(self.span)*LF

                                # get deflection at each interior support location
                                for i, j in enumerate(self.interiorSupports):
                                    intDelta[i]+= load.eidx(j)*LF
                                
                                # determine the reactions from the current load
                                rltemp += load.rl*LF
                                rrtemp += load.rr*LF
                                
                                # determine the fixed end forces
                                feftemp = [i+(j*LF) for i,j in zip(feftemp,load.fef())]
                                
                                # determine the loads piecewise functions
                                load_functions = load.piece_functions()
                                
                                # combine the current loads functions
                                # with the piecewise functions for the beam
                                vfunctemp = bmtools.combine_piecewise_functions(vfunctemp, load_functions[0], 1, LF)
                                mfunctemp = bmtools.combine_piecewise_functions(mfunctemp, load_functions[1], 1, LF)
                                eisfunctemp = bmtools.combine_piecewise_functions(eisfunctemp, load_functions[2], 1, LF)
                                eidfunctemp = bmtools.combine_piecewise_functions(eidfunctemp, load_functions[3], 1, LF)
                                
                        else:
                            # Load type is not part of the current combo
                            pass

                    # we have looped through all of the loads and aggregated
                    # the end slopes and deflections at the interior supports
                    # use the flexibibility method to solve for the redundant
                    # reactions.
                    
                    if self.endCondition==[0,0] and self.interiorSupports==[]:
                        
                        # if no end fixity and no interior supports then there
                        # is no reason to run the flexibility solver.
                        
                        redundants = []
                    
                    else:
                        
                        # solve for the redundant reactions using the flexibility
                        # solver
                        deformations = []
                        deformations.extend(endSlopes)
                        deformations.extend(intDelta)
    
                        redundants, reaction_loads = solve2d.flexibility_solver(deformations,self.interiorSupports,self.span,self.endCondition,f'{combo_key}{pattern_key}',self.id)
                    
                        for reaction in reaction_loads:
                            rltemp += reaction.rl
                            rrtemp += reaction.rr
                            
                            load_functions = reaction.piece_functions()
                            
                            vfunctemp = bmtools.combine_piecewise_functions(vfunctemp, load_functions[0], 1, 1)
                            mfunctemp = bmtools.combine_piecewise_functions(mfunctemp, load_functions[1], 1, 1)
                            eisfunctemp = bmtools.combine_piecewise_functions(eisfunctemp, load_functions[2], 1, 1)
                            eidfunctemp = bmtools.combine_piecewise_functions(eidfunctemp, load_functions[3], 1, 1)
                    
                    rdict[f'{pattern_key}'] = {'rl':rltemp,'rr':rrtemp, 'redundants':redundants}
                    fefdict[f'{pattern_key}'] = {'FL':feftemp[0],"ML":feftemp[1],"FR":feftemp[2],"MR":feftemp[3]}
                    vfunc[f'{pattern_key}'] = vfunctemp
                    mfunc[f'{pattern_key}'] = mfunctemp
                    eisfunc[f'{pattern_key}'] = eisfunctemp
                    eidfunc[f'{pattern_key}'] = eidfunctemp
                    
                    shear_roots = bmtools.roots_piecewise_function(vfunctemp)
                    slope_roots = bmtools.roots_piecewise_function(eisfunctemp)
                    
                    self.rootstations.extend(shear_roots)
                    self.rootstations.extend(slope_roots)
                    
                if combo.combo_type == None:
                    self.reactions_basic[combo_key] = rdict
                    self.v_functions_basic[combo_key] = vfunc
                    self.m_functions_basic[combo_key] = mfunc
                    self.eis_functions_basic[combo_key] = eisfunc
                    self.eid_functions_basic[combo_key] = eidfunc
                    self.FEF_basic[combo_key] = fefdict
                
                elif combo.combo_type == 'ULS':
                    self.reactions_uls[combo_key] = rdict
                    self.v_functions_uls[combo_key] = vfunc
                    self.m_functions_uls[combo_key] = mfunc
                    self.FEF_uls[combo_key] = fefdict
                
                elif combo.combo_type == 'SLS':
                    self.reactions_sls[combo_key] = rdict
                    self.v_functions_sls[combo_key] = vfunc
                    self.m_functions_sls[combo_key] = mfunc
                    self.eis_functions_sls[combo_key] = eisfunc
                    self.eid_functions_sls[combo_key] = eidfunc
                    self.FEF_sls[combo_key] = fefdict
                
                # with large numbers of patterns too much precision on the roots
                # leads to large result arrays, round to the 4th decimal place
                # as a compromise. Inform users this was done in GUI.
                # 4 decimal places is equivalent to 0.0012 inches or
                # 0.01 mm if using metric, where the length basis is
                # feet for imperial and meters for metric
                
                self.rootstations = [round(i,4) for i in self.rootstations]
                
                self.rootstations = sorted(set(self.rootstations))
                
                self.printstations.extend(self.calcstations)
                self.printstations.extend(self.rootstations)
                
                self.printstations = sorted(set(self.printstations))
                self.chartstations = [i+self.node_i.x for i in self.printstations]
                
                self.analyzed = True

    def ULS_envelopes(self):
        
        if self.analyzed:
            
            i = 0
            for key, value in self.v_functions_uls.items():
                
                for patern, piece_function in value.items():
                    
                    vtemp = [bmtools.eval_piece_function(piece_function, j) for j in self.printstations]
                    
                    if i == 0:
                        
                        self.Vu_max = [j for j in vtemp]
                        self.Vu_min = [j for j in vtemp]
                        i+=1
                    
                    else:
                        self.Vu_max = [max(k,j) for k,j in zip(self.Vu_max,vtemp)]
                        self.Vu_min = [min(k,j) for k,j in zip(self.Vu_min,vtemp)]
                        
            i = 0
            for key, value in self.m_functions_uls.items():
                
                for patern, piece_function in value.items():
                    
                    mtemp = [bmtools.eval_piece_function(piece_function, j) for j in self.printstations]
                    
                    if i == 0:
                        
                        self.Mu_max = [j for j in mtemp]
                        self.Mu_min = [j for j in mtemp]
                        i+=1
                    
                    else:
                        self.Mu_max = [max(k,j) for k,j in zip(self.Mu_max,mtemp)]
                        self.Mu_min = [min(k,j) for k,j in zip(self.Mu_min,mtemp)]

    def SLS_envelopes(self, conv = 12):
        '''
        Function to evaluate the pieweise SLS functions
        
        conv input is a multiplier on the deflection input, default of 12 assumes
        that the basis of length units was feet.
        '''
        
        if self.analyzed:
            
            i = 0
            for key, value in self.v_functions_sls.items():
                
                for patern, piece_function in value.items():
                    
                    vtemp = [bmtools.eval_piece_function(piece_function, j) for j in self.printstations]
                    
                    if i == 0:
                        
                        self.Vs_max = [j for j in vtemp]
                        self.Vs_min = [j for j in vtemp]
                        i+=1
                    
                    else:
                        self.Vs_max = [max(k,j) for k,j in zip(self.Vs_max,vtemp)]
                        self.Vs_min = [min(k,j) for k,j in zip(self.Vs_min,vtemp)]
                        
            i = 0
            for key, value in self.m_functions_sls.items():
                
                for patern, piece_function in value.items():
                    
                    mtemp = [bmtools.eval_piece_function(piece_function, j) for j in self.printstations]
                    
                    if i == 0:
                        
                        self.Ms_max = [j for j in mtemp]
                        self.Ms_min = [j for j in mtemp]
                        i+=1
                    
                    else:
                        self.Ms_max = [max(k,j) for k,j in zip(self.Ms_max,mtemp)]
                        self.Ms_min = [min(k,j) for k,j in zip(self.Ms_min,mtemp)]
                
            i = 0
            for key, value in self.eis_functions_sls.items():
                
                for patern, piece_function in value.items():
                    
                    eistemp = [bmtools.eval_piece_function(piece_function, j) for j in self.printstations]
                    
                    if i == 0:
                        
                        self.Ss_max = [j/(self.Em*self.Ixx) for j in eistemp]
                        self.Ss_min = [j/(self.Em*self.Ixx) for j in eistemp]
                        i+=1
                    
                    else:
                        self.Ss_max = [max(k,j/(self.Em*self.Ixx)) for k,j in zip(self.Ss_max,eistemp)]
                        self.Ss_min = [min(k,j/(self.Em*self.Ixx)) for k,j in zip(self.Ss_min,eistemp)]
                        
            i = 0
            for key, value in self.eid_functions_sls.items():
                
                for patern, piece_function in value.items():
                    
                    eidtemp = [bmtools.eval_piece_function(piece_function, j) for j in self.printstations]
                    
                    if i == 0:
                        
                        self.Ds_max = [(conv*j)/(self.Em*self.Ixx) for j in eidtemp]
                        self.Ds_min = [(conv*j)/(self.Em*self.Ixx) for j in eidtemp]
                        i+=1
                    
                    else:
                        self.Ds_max = [max(k,(conv*j)/(self.Em*self.Ixx)) for k,j in zip(self.Ds_max,eidtemp)]
                        self.Ds_min = [min(k,(conv*j)/(self.Em*self.Ixx)) for k,j in zip(self.Ds_min,eidtemp)]

# Test Area #

# if __name__== '__main__':
    
#     E_ksi = 29000
#     E_ksf = E_ksi * 144 # 144 in2/ 1 ft2

#     I_in4 = 30.8
#     I_ft4 = I_in4 * (1/math.pow(12,4))

#     n1 = g2d.Node2D(20, 0, "N1", 1)
#     n2 = g2d.Node2D(30, 0, "N2", 2)

#     beam = Beam2D("BM1", n1, n2, E_ksf, I_ft4,[0,0],3)

#     # beam.addinteriorsupport(10)
#     # beam.addinteriorsupport(20)
#     # beam.addinteriorsupport(30)
#     # beam.addinteriorsupport(40)
#     # beam.addinteriorsupport(50)

#     # print(beam.spans())

#     beam.computation_stations()


#     #combo1 = LC.LoadCombo("combo1",{"D":1.2,"L":1.6},["L"],True,'ULS')
#     #combo2 = LC.LoadCombo("combo2",{"L":1.0},["L"],True,'SLS')
#     #combo3 = LC.LoadCombo('all D',{'D':1.0,"L":1.0},['L'],False,'ULS')

#     uls_combos = LC.IBC2018_ULS(1, 0.7, True)
#     sls_combos = LC.IBC2018_ASD(True,True)
#     basic_combos = LC.IBC2018_Basic(True,False)


#     load1 = ebl.cant_right_udl(1, 0, 10, beam.span,0, "L", 3)
#     load2 = ebl.cant_right_udl(0.5, 0, 10, beam.span,0, "D", 3)
#     load3 = ebl.cant_right_point(1, 2, beam.span, 0, "Ex", 3)

#     loads = [load1,load2,load3]

#     # load1 = ebl.udl(1, 0, 10, beam.span, "L", 1)
#     # load2 = ebl.udl(1, 10, 20, beam.span, "L", 2)
#     # load3 = ebl.udl(1, 20, 30, beam.span, "L", 3)
#     # load4 = ebl.udl(1, 30, 40, beam.span, "L", 4)
#     # load5 = ebl.udl(1, 40, 50, beam.span, "L", 5)
#     # load6 = ebl.udl(1, 50, 60, beam.span, "L", 6)
#     # load7 = ebl.udl(1, 50, 60, beam.span, "D", 6)
#     # load8 = ebl.udl(1, 0, 10, beam.span, "D", 1)

#     # loads = [load1,load2,load3,load4,load5, load6, load7, load8]

#     applied_loads = {"D":False,
#                      "F":False,
#                      "L":False,
#                      "H":False,
#                      "Lr":False,
#                      "S":False,
#                      "R":False,
#                      "Wx":False,
#                      "Wy":False,
#                      "Ex":False,
#                      "Ey":False}

#     for load in loads:
        
#         if load.loadtype in applied_loads:
#             if not applied_loads[load.loadtype]:
                
#                 applied_loads[load.loadtype] = True
        
#     uls_combos_trim = []
#     for combo in uls_combos:
        
#         test = []
#         for kind in combo.principle_loads:
            
#             test.append(applied_loads[kind])
    
#         if any(test):
            
#             uls_combos_trim.append(combo)
            
#     print('Reduced ULS Combinations:')
#     for combo in uls_combos_trim:
#         print(combo.FormulaString())  
        
#     sls_combos_trim = []
#     for combo in sls_combos:
        
#         test = []
#         for kind in combo.principle_loads:
            
#             test.append(applied_loads[kind])
    
#         if any(test):
            
#             sls_combos_trim.append(combo)
            
#     print('Reduced SLS Combinations:')
#     for combo in sls_combos_trim:
#         print(combo.FormulaString()) 
                

#     basic_combos_trim = []
#     for combo in basic_combos:
        
#         test = []
#         for kind in combo.principle_loads:
            
#             test.append(applied_loads[kind])
    
#         if any(test):
            
#             basic_combos_trim.append(combo)
            
#     print('Reduced BASIC Combinations:')
#     for combo in basic_combos_trim:
#         print(combo.FormulaString()) 

#     patterns = LC.Full_LoadPatterns(3)
#     aci_pats = LC.ACI_LoadPatterns(3, False)

#     off_patt = {"L":0}

#     beam.addLoads(loads)

#     beam.flexibility_analyze(uls_combos_trim,patterns,off_patt)
#     beam.flexibility_analyze(basic_combos_trim,patterns,off_patt)
#     beam.flexibility_analyze(sls_combos_trim,patterns,off_patt)

#     beam.ULS_envelopes()
#     beam.SLS_envelopes()

#     fig, ax1 = plt.subplots()

#     ax1.plot(beam.chartstations,beam.Ds_max, linewidth=2.0)
#     ax1.plot(beam.chartstations,beam.Ds_min, linewidth=1.0)

#     plt.show()
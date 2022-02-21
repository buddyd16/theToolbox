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

import enum
import analysis.geometry2D as g2d
import analysis.ebloads as ebl
import analysis.loadcombos as LC
import analysis.flexibility2D as solve2d


class Beam2D():
    '''
    A class representing a 2D - Euler-Bernoulli Beam
    '''

    def __init__(self, userName, node_i, node_j, Em, Ixx, endCondition=[0, 0], span):

        self.userName = userName            # User defined name
        self.node_i = node_i                # Beam i node (x,y)
        self.node_j = node_j                # Beam j node (x,y)
        self.Em = Em                        # Beam modulus of elasticity
        self.Ixx = Ixx                      # Beam moment of inertia about
                                            # the axis of bending
        self.endCondition = endCondition    # Beam end condition 1-fixed 0-pin

        self.span = span                    # The span id of this beam

        # Initiliaze empty data sets for other variable beam info
        self.interiorSupports = []  # List of additional support locations, as a 
                                    # relative distance from the i end along beam.
        self.Loads = []             # List to hold the applied loads
        self.reactions_basic = {}   # Dictionary to hold Basic reactions
        self.reactions_uls = {}     # Dictionary to hold ULS reactions
        self.reactions_sls = {}     # Dictionary to hold Service Reactions
        self.Mu_max = []            # List to hold Mu,max (ULS Moment Envelope)
        self.Mu_min = []            # List to hold Mu,min (ULS Moment Envelope)
        self.Vu_max = []            # List to hold Vu,max (ULS Shear Envelope)
        self.Vu_min = []            # List to hold Vu,min (ULS Shear Envelope)
        self.Ms_max = []            # List to hold Ms,max (Service Moment Envelope)
        self.Ms_min = []            # List to hold Ms,min (Service Moment Envelope)
        self.Vs_max = []            # List to hold Vs,max (Service Shear Envelope)
        self.Vs_min = []            # List to hold Vs,min (Service Shear Envelope)
        self.S_min = []             # List to hold Slope,min (Service Envelope)
        self.S_max = []             # List to hold Slope,max (Service Envelope)
        self.D_min = []             # List to hold Deflection,min (Service Envelope)
        self.D_max = []             # List to hold Deflection,max (Service Envelope)

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

    def computation_stations(self, num_stations=42):
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

        self.calcstations = list(set(stations))
        self.calcstations.sort()

        # populate the diagram lists with 0 in a equal quantity to the calculation
        # stations

        self.Mu_max = [0 for e in self.calcstations]
        self.Mu_min = [0 for e in self.calcstations]
        self.Vu_max = [0 for e in self.calcstations]
        self.Vu_min = [0 for e in self.calcstations]
        self.Ms_max = [0 for e in self.calcstations]
        self.Ms_min = [0 for e in self.calcstations]
        self.Vs_max = [0 for e in self.calcstations]
        self.Vs_min = [0 for e in self.calcstations]
        self.S_min = [0 for e in self.calcstations]
        self.S_max = [0 for e in self.calcstations]
        self.D_min = [0 for e in self.calcstations]
        self.D_max = [0 for e in self.calcstations]
    
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

                if combo.patterned == True and (self.span != 1 or self.interiorSupports !=[]):

                    # we only need to pattern loads if the beam is not the only beam
                    # or if there are interior supports

                    for pattern  in patterns:
                        
                        endSlopes = [0, 0]
                        intDelta = [0 for i in self.interiorSupports]

                        mtemp = [0 for i in self.calcstations]
                        vtemp = [0 for i in self.calcstations]
                        stemp = [0 for i in self.calcstations]
                        dtemp = [0 for i in self.calcstations]

                        pattern_key = pattern
                        
                        for load in self.Loads:
                            if load.loadtype in combo.factors:
                                # Load type is part of the current combo
                                LF = combo.factors[load.loadtype]
                                
                                if self.loadtype in offpatternfactors:
                                    # if the load type exists in the offpattern
                                    # factor list then the load is a type that 
                                    # should be pattterned
                                    LFoffpat = offpatternfactors[self.loadtype]

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
                                    
                                    # fill in v,m,s,d at station values
                                    # do this now so that we only need to add in
                                    # the contribution of the interior reactions
                                    # and end moments later instead of repeat
                                    # this whole loop.
                                    for i, j in enumerate(self.calcstations):
                                        vtemp[i] += load.v(j)*LF
                                        mtemp[i] += load.m(j)*LF
                                        stemp[i] += load.eisx(j)*LF
                                        dtemp[i] += load.eidx(j)*LF
                            else:
                                # Load type is not part of the current combo
                                pass

                        # we have looped through all of the loads and aggregated
                        # the end slopes and deflections at the interior supports






# Test Area #

n1 = geometry2D.Node2D(0, 0, "N1", 1)
n2 = geometry2D.Node2D(30, 0, "N2", 2)

print(n1)
print(n2)

beam = Beam2D("BM1", n1, n2, 29000, 30.8)

beam.addinteriorsupport(10.3)
beam.addinteriorsupport(19.5)

print(beam.spans())

beam.computation_stations()

print(beam.calcstations)
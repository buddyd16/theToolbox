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

# These imports are for when flask is live

import analysis.geometry2D as g2d
import analysis.ebloads as ebl
import analysis.loadcombos as LC
import analysis.flexibility2D as solve2d
import analysis.beamtools as bmtools
import analysis.beam2D as b2d

# These imports are for local use

# import beam2D as b2d
# import geometry2D as g2d
# import ebloads as ebl
# import loadcombos as LC
# import flexibility2D as solve2d
# import beamtools as bmtools

import math


def SimpleBeam(inputs):

    LoadKinds = ['D', 'F', 'L', 'H', 'Lr', 'S', 'R', 'Wx', 'Wy', 'Ex', 'Ey']

    # applied load dictionary to track what types of loads are
    # applied to the beam. This will be used to filter the load
    # combinations later.

    applied_loads = {"D": False,
                     "F": False,
                     "L": False,
                     "H": False,
                     "Lr": False,
                     "S": False,
                     "R": False,
                     "Wx": False,
                     "Wy": False,
                     "Ex": False,
                     "Ey": False}

    ###########################################################################
    # Loads Pre-Process
    ###########################################################################

    # List the non-0 loads
    Loads = []

    for distLoad in inputs['distLoads']:
        # Form input asks for tributary width and pressure
        # Convert this to KLF
        w1 = distLoad[0]*distLoad[1]*(1/1000)  # 1 klf / 1000 plf
        w2 = distLoad[2]*distLoad[3]*(1/1000)  # 1 klf / 1000 plf
        a = distLoad[4]
        b = distLoad[5]
        k = distLoad[6]
        type = "TRAP"

        if w1 == 0 and w2 == 0:
            # there is a chance that the user entered a 0 trib
            # this will catch that and not add a load of 0's to
            # the load list
            pass
        else:
            # Type will always be index[0]
            # Kind will always be index[-1]
            Loads.append([type, w1, w2, a, b, k])

            # flip switch on applied loads type
            if k in applied_loads:
                if not applied_loads[k]:
                    applied_loads[k] = True

    for ptLoad in inputs['pointLoads']:
        p = ptLoad[0]
        a = ptLoad[1]
        k = ptLoad[2]
        type = "POINT"

        if p == 0:
            # 0 loads can still be passed to the function
            # catch them here
            pass
        else:
            Loads.append([type, p, a, k])

            # flip switch on applied loads type
            if k in applied_loads:
                if not applied_loads[k]:
                    applied_loads[k] = True

    for ptMoment in inputs['pointMoments']:
        m = ptMoment[0]
        a = ptMoment[1]
        k = ptMoment[2]
        type = "MOMENT"

        if m == 0:
            # 0 Moments can still be passed to the function
            # catch them here
            pass
        else:
            Loads.append([type, m, a, k])

            # flip switch on applied loads type
            if k in applied_loads:
                if not applied_loads[k]:
                    applied_loads[k] = True

    ###########################################################################
    # End Loads Pre-Process
    ###########################################################################

    ###########################################################################
    # Create and Process the Load Combinations
    ###########################################################################

    # Combo parameters
    IBC_f1 = inputs['f1']
    IBC_f2 = inputs['f2']

    if inputs['latReverse'] == 1:
        lateralReverse = True
    else:
        lateralReverse = False

    # Design Load Combinations
    if inputs['combos'] == 0:
        uls_combos_bulk = LC.IBC2018_ASD(lateralReverse, False)
    else:
        uls_combos_bulk = LC.IBC2018_ULS(IBC_f1, IBC_f2, lateralReverse)

    # User defined Service Combinations
    sls_combos = []

    for i, userCombo in enumerate(inputs['sls']):
        userid = f'S{i}'

        loadFactors = {}
        pattern = []
        for j, factor in enumerate(userCombo):
            if factor == 0:
                pass
            else:
                loadFactors[LoadKinds[j]] = factor
                if LoadKinds[j] in ['L', 'Lr', 'S', 'R']:
                    pattern = True

        sls_combos.append(LC.LoadCombo(userid, loadFactors,
                                       patterned=pattern, combo_type='SLS'))

    # Basic Combos
    basic_combos_bulk = LC.IBC2018_Basic(lateralReverse, False)

    # Trim out ULS Combos
    uls_combos = []
    for combo in uls_combos_bulk:
        test = []
        for kind in combo.principle_loads:
            test.append(applied_loads[kind])
        if any(test):
            uls_combos.append(combo)

    print('Reduced ULS Combinations:')
    for combo in uls_combos:
        print(combo.FormulaString())

    # Trim out Basic Combos
    basic_combos = []
    for combo in basic_combos_bulk:
        test = []
        for kind in combo.principle_loads:
            test.append(applied_loads[kind])
        if any(test):
            basic_combos.append(combo)

    print('Reduced Basic Combinations:')
    for combo in basic_combos:
        print(combo.FormulaString())

    ###########################################################################
    # End of the Load Combination Processing
    ###########################################################################

    ###########################################################################
    # Begin Geometry
    ###########################################################################

    # Get the material and section properties
    # and convert them to a consistent unit set
    # Use Kips and Feet for Imperial units
    # !!! Need to Convert Deflection Results back to inches !!!
    E_ksi = inputs['E']
    E_ksf = E_ksi * 144  # 144 in2/ 1 ft2

    I_in4 = inputs['I']
    I_ft4 = I_in4 * (1/math.pow(12, 4))  # 1 ft^4 / 12^4 in^4

    # No matter what node1 is at (x,y) = (0,0)
    nodes = []
    n1 = g2d.Node2D(0, 0, "N1", 1)
    nodes.append(n1)

    overhangLeft_ft = inputs['OverL']

    # Central span data
    mainSpan_ft = inputs['span']
    interiorSupports_ft = []
    for loc in inputs['intSups']:
        # a value of 0 for the interior support will
        # pass through to the function. catch those here
        if loc == 0:
            pass
        else:
            interiorSupports_ft.append(loc)

    # sort the interior support list to avoid issues later
    interiorSupports_ft.sort()

    endFixity = [inputs['fl'], inputs['fr']]

    overhangRight_ft = inputs['OverR']

    # Total number of spans inclusive of cantilevers and interiors
    num_spans = len(interiorSupports_ft)+1
    if overhangLeft_ft != 0:
        num_spans += 1

    if overhangRight_ft != 0:
        num_spans += 1

    print(f'# Spans: {num_spans}')

    if overhangLeft_ft != 0:
        n2 = g2d.Node2D(overhangLeft_ft, 0, "N2", 2)
        nodes.append(n2)
        cantLeft = b2d.Beam2D("cantLeft", n1, n2, E_ksf, I_ft4, [0, 0], 0)
        x3 = overhangLeft_ft + mainSpan_ft
        n3 = g2d.Node2D(x3, 0, "N3", 3)
        nodes.append(n3)
        mainBeam = b2d.Beam2D("mainBeam", n2, n3, E_ksf, I_ft4, endFixity, 2)

        if overhangRight_ft != 0:
            x4 = x3 + overhangRight_ft
            n4 = g2d.Node2D(x4, 0, "N4", 4)
            nodes.append(n4)
            cantRight = b2d.Beam2D("cantRight", n3, n4,
                                   E_ksf, I_ft4, [0, 0], num_spans)
        else:
            cantRight = None
    else:
        n2 = g2d.Node2D(mainSpan_ft, 0, "N2", 2)
        nodes.append(n2)
        cantLeft = None

        if overhangRight_ft != 0:
            mainBeam = b2d.Beam2D("mainBeam", n1, n2,
                                  E_ksf, I_ft4, endFixity, 0)
            x3 = mainSpan_ft + overhangRight_ft
            n3 = g2d.Node2D(x3, 0, "N3", 3)
            nodes.append(n3)
            cantRight = b2d.Beam2D("cantRight", n2, n3,
                                   E_ksf, I_ft4, [0, 0], num_spans)
        else:
            cantRight = None
            mainBeam = b2d.Beam2D("mainBeam", n1, n2,
                                  E_ksf, I_ft4, endFixity, 1)

    # add the iterior supports to the main beam
    for support in interiorSupports_ft:
        mainBeam.addinteriorsupport(support)

    # Determine the load patterns
    # If the number of spans exceeds 6 use the simplified (6)ACI patters
    if num_spans < 7:
        patterns = LC.Full_LoadPatterns(num_spans)
    else:
        patterns = LC.ACI_LoadPatterns(num_spans, False)

    print('Load Patterns:')
    print(patterns)

    # set the offPattern dictionary
    off_patt = {"L": inputs['offPat'][0],
                "Lr": inputs['offPat'][1],
                "S": inputs['offPat'][2],
                "R": inputs['offPat'][3], }

    ###########################################################################
    # End Geometry
    ###########################################################################

    ###########################################################################
    # Process the Loads to their analytical class
    ###########################################################################

    # Get the main beam span set inlcuding interior supports
    mainSpans = mainBeam.spans()

    # list of ascending values of span numbers
    spanIDs = [1+i for i in range(num_spans)]

    # globalSpans will be an ordered list of ascending values
    # indicating the end x location of each span
    globalSpans = []

    if cantLeft is not None:
        globalSpans.append(cantLeft.span)

    for i, span in enumerate(mainSpans):
        if globalSpans == [] and i == 0:
            globalSpans.append(span)
        else:
            globalSpans.append(span+globalSpans[-1])

    if cantRight is not None:
        globalSpans.append(cantRight.span+globalSpans[-1])

    cantLeftLoads = []
    mainbeamLoads = []
    cantRightLoads = []

    for load in Loads:

        type = load[0]
        kind = load[-1]

        ##############################
        # Point and Moment Load Types
        ##############################
        if type == "POINT" or type == "MOMENT":
            p = load[1]
            a = load[2]
            # Get the index of the span start point
            # that is greater than a
            globalIndex = next(x for x, val in enumerate(globalSpans) if val >= a)
            loadspanID = spanIDs[globalIndex]

            if cantLeft is not None and loadspanID == 1:
                if type == "POINT":
                    cantLeftLoads.append(ebl.cant_left_point(
                        p, a, cantLeft.span, 0, kind, loadspanID))

                    # Capture the end moment and shear applied to
                    # the main span from the cantilever load here
                    m = cantLeftLoads[-1].mr
                    mainbeamLoads.append(ebl.point_moment(
                        m, 0, mainBeam.span, kind, loadspanID))
                    mainbeamLoads.append(
                        ebl.pl(p, 0, mainBeam.span, kind, loadspanID))

                else:
                    cantLeftLoads.append(ebl.cant_left_point_moment(
                        p, a, cantLeft.span, 0, kind, loadspanID))

                    # Capture the end moment and shear applied to
                    # the main span from the cantilever load here
                    m = cantLeftLoads[-1].mr
                    mainbeamLoads.append(ebl.point_moment(
                        m, 0, mainBeam.span, kind, loadspanID))

            elif cantRight is not None and loadspanID == spanIDs[-1]:
                # if this is the right cantilever we need to subtract out
                # the x coordinate of the right most support from a
                # to give a in terms of the local length of the beam.
                xa = a - nodes[-2].x
                if type == "POINT":
                    cantRightLoads.append(ebl.cant_right_point(
                        p, xa, cantRight.span, 0, kind, loadspanID))

                    # Capture the end moment and shear applied to
                    # the main span from the cantilever load here
                    m = -1*cantRightLoads[-1].ml
                    mainbeamLoads.append(ebl.point_moment(
                        m, mainBeam.span, mainBeam.span, kind, loadspanID))
                    mainbeamLoads.append(ebl.pl(
                            p, mainBeam.span, mainBeam.span, kind, loadspanID))
                else:
                    cantRightLoads.append(ebl.cant_right_point_moment(
                        p, xa, cantRight.span, 0, kind, loadspanID))

                    # Capture the end moment and shear applied to
                    # the main span from the cantilever load here
                    m = -1*cantRightLoads[-1].ml
                    mainbeamLoads.append(ebl.point_moment(
                        m, mainBeam.span, mainBeam.span, kind, loadspanID))
            else:
                # checked if cantilevers were active and the spanID matched
                # only remaining option is the load is in the main span

                # knowing the load is in the main span
                # subtract the left support node x value from a
                # if there is no left overhange then we will be subtracting 0
                # This will get the load point relative to the main beam local span
                xa = a - mainBeam.node_i.x

                if type == "POINT":
                    mainbeamLoads.append(
                        ebl.pl(p, xa, mainBeam.span, kind, loadspanID))
                else:
                    mainbeamLoads.append(
                        ebl.point_moment(p, xa, mainBeam.span, kind, loadspanID))

            ##############################
            # End Point and Moment Load Types
            ##############################

            ##############################
            # Variable (TRAP) Load Types
            ##############################
        else:
            # Only Load types entering function are TRAP,POINT,MOMENT
            # alreaddy checked above for POINT and MOMENT so no need for
            # an elif here, just need the else.

            # [type, w1, w2, a, b, k]
            # [0,1,2,3,4,5]
            w1 = load[1]
            w2 = load[2]
            a = load[3]
            b = load[4]

            # Since the load is applied over some finite length
            # step through each span and solve the parametric eqn
            # for the load length for t, if t is between 0 and 1
            # then all or a portion of the load applies in the span
            for i, span in enumerate(globalSpans):
                # span = a + t (b-a)
                # t < 0 then load starts after current span
                # t >= 1 then the whole load is before the span
                t = (span - a)/(b-a) # whoops need to validate b-a != 0

                if t < 0:
                    # load starts after span
                    pass
                elif i == 0 and t >= 0:
                    # entire load is in the first span
                    if t > 1:
                        # load entirely in the first span
                        if cantLeft is not None:
                            # load applies to the cantilever
                            cantLeftLoads.append(
                                ebl.cant_left_trap(w1,w2,a,b,cantLeft.span,0,kind,spanIDs[i]))
                            # Catch the loads at the support from the cantilever
                            # here and apply them to the ebam
                            p = cantLeftLoads[-1].rr
                            m = cantLeftLoads[-1].mr
                            mainbeamLoads.append(
                                ebl.pl(p,0,mainBeam.span,kind,spanIDs[i]))
                            mainbeamLoads.append(
                                ebl.point_moment(m,0,mainBeam.span,kind,spanIDs[i]))
                        
                        else:
                            # limitation of the app is you need a main span to have
                            # a right cantilever, and globalSpans includes the
                            # interior spans of the main span so we can apply
                            # the load to the whole first span and it will be on
                            # the mainbeam and in the mainbeams local coordinates.

                            mainbeamLoads.append(
                                ebl.trap(w1,w2,a,b,mainBeam.span,kind,spanIDs[i]))
                    else:
                        # load extends beyond first span
                        # interpolate w2
                        wc = w1 + (t*(w2-w1))
                        c = span

                        if cantLeft is not None:
                            # load applies to the cantilever
                            cantLeftLoads.append(
                                ebl.cant_left_trap(w1,wc,a,c,cantLeft.span,0,kind,spanIDs[i]))
                            # Catch the loads at the support from the cantilever
                            # here and apply them to the ebam
                            p = cantLeftLoads[-1].rr
                            m = cantLeftLoads[-1].mr
                            mainbeamLoads.append(
                                ebl.pl(p,0,mainBeam.span,kind,spanIDs[i]))
                            mainbeamLoads.append(
                                ebl.point_moment(m,0,mainBeam.span,kind,spanIDs[i]))
                        else:
                            # limitation of the app is you need a main span to have
                            # a right cantilever, and globalSpans includes the
                            # interior spans of the main span so we can apply
                            # the load to the whole first span and it will be on
                            # the mainbeam and in the mainbeams local coordinates.

                            mainbeamLoads.append(
                                ebl.trap(w1,wc,a,c,mainBeam.span,kind,spanIDs[i]))

                elif span != globalSpans[-1] and t > 0:
                    # if we are not in the end span and we are not in the first
                    # span then we are at some intermediate span within the main
                    # span.

                    # determine t for the previous span
                    tp = (globalSpans[i-1]-a)/(b-a)

                    # tp < 0 load starts in the span
                    # tp >= 0 load starts at or prior to the span
                    if tp <= 0:
                        # the load starts in or at this span
                        # subtract the left support x from a to get
                        # a in the local system of the mainbeam
                        xa = a - mainBeam.node_i.x
                        
                        # determine if w2 needs to be truncated
                        if t <= 1:
                            # then then the load encompasses the span
                            # interpolate w2 and b
                            wc = w1 + (t*(w2-w1))
                            c = a + (t*(b-a))

                            # c is in the global system need to subtract the 
                            # left support x to get it to local
                            xc = c - mainBeam.node_i.x

                            mainbeamLoads.append(
                                ebl.trap(w1,wc,xa,xc,mainBeam.span,kind,spanIDs[i]))
                        else:
                            # other option is t > 1 which means the load ends
                            # in this span, and W2 does not need to be interpolated

                            # b is in the global system need to subtract the 
                            # left support x to get it to local
                            xb = b - mainBeam.node_i.x

                            mainbeamLoads.append(
                                ebl.trap(w1,w2,xa,xb,mainBeam.span,kind,spanIDs[i]))
                    else:
                        # the load started prior to this span
                        # interpolate w1
                        wc = w1 + (tp*(w2-w1))
                        # locally the load start point is the span start point
                        xc = globalSpans[i-1] - mainBeam.node_i.x

                        if t<=1:
                            # then the load encompasses the span
                            # interpolate w2 and b
                            wd = w1 + (t*(w2-w1))
                            d = a + (t*(b-a))

                            xd = d - mainBeam.node_i.x

                            mainbeamLoads.append(
                                ebl.trap(wc,wd,xc,xd,mainBeam.span,kind,spanIDs[i]))
                        elif t>1 and tp>=1:
                            # Loads ends at the beginning of this span
                            pass
                        else:
                            # other option is t>1 which means the load ends
                            # in this span, and W2 does not require interpolation

                            xb = b - mainBeam.node_i.x

                            mainbeamLoads.append(
                                ebl.trap(wc,w2,xc,xb,mainBeam.span,kind,spanIDs[i]))

                elif span == globalSpans[-1] and t > 0:
                    # we are in the last span
                    # determine t for the previous span
                    tp = (globalSpans[i-1]-a)/(b-a)

                    # tp < 0 load starts in the span
                    # tp >= 0 load starts at or prior to the span
                    if tp <= 0:
                        # load starts at or in this span

                        if cantRight is not None:
                            # a needs to be converted to the cantilever
                            # local system
                            xa = a - mainBeam.node_j.x

                            # assume the load end point was not allowed
                            # to go off the beam end
                            xb = b - mainBeam.node_j.x

                            cantRightLoads.append(
                                ebl.cant_right_trap(w1,w2,xa,xb,cantRight.span,0,kind,spanIDs[i]))
                            
                            # Capture the end moment and shear applied to
                            # the main span from the cantilever load here
                            m = -1*cantRightLoads[-1].ml
                            p = cantRightLoads[-1].rl
                            mainbeamLoads.append(ebl.point_moment(
                                m, mainBeam.span, mainBeam.span, kind, spanIDs[i]))
                            mainbeamLoads.append(ebl.pl(
                                    p, mainBeam.span, mainBeam.span, kind, spanIDs[i]))
                        else:
                            # we are in the last span of the main beam
                            xa = a - mainBeam.node_i.x
                            xb = b - mainBeam.node_i.x

                            mainbeamLoads.append(
                                ebl.trap(w1,w2,xa,xb,mainBeam.span,kind,spanIDs[i])
                            )
                    else:
                        # Loaded started prior to this span
                        # interpolate w1
                        wc = w1 + (tp*(w2-w1))

                        if cantRight is not None:
                            # locally the load start point is the span start point
                            xc = globalSpans[i-1] - mainBeam.node_j.x

                            # assume the load end point was not allowed
                            # to go off the beam end
                            xb = b - mainBeam.node_j.x

                            cantRightLoads.append(
                                ebl.cant_right_trap(wc,w2,xc,xb,cantRight.span,0,kind,spanIDs[i]))

                            # Capture the end moment and shear applied to
                            # the main span from the cantilever load here
                            m = -1*cantRightLoads[-1].ml
                            p = cantRightLoads[-1].rl
                            mainbeamLoads.append(ebl.point_moment(
                                m, mainBeam.span, mainBeam.span, kind, spanIDs[i]))
                            mainbeamLoads.append(ebl.pl(
                                    p, mainBeam.span, mainBeam.span, kind, spanIDs[i]))
                        else:
                            # we are in the last beam span
                            xc = globalSpans[i-1] - mainBeam.node_i.x
                            xb = b - mainBeam.node_i.x

                            mainbeamLoads.append(
                                ebl.trap(wc,w2,xc,xb,mainBeam.span,kind,spanIDs[i]))

                else:
                    # if we don't meet any of the previous criteria maybe the
                    # load data is bad, so just skip it
                    pass

    ###########################################################################
    # End Process the Loads to their analytical class
    ###########################################################################

    ###########################################################################
    # Apply Loads to the beams
    ###########################################################################

    if cantLeft is not None:
        cantLeft.addLoads(cantLeftLoads)
    
    if cantRight is not None:
        cantRight.addLoads(cantRightLoads)
    
    mainBeam.addLoads(mainbeamLoads)

    ###########################################################################
    # End Apply Loads to the beams
    ###########################################################################

    ###########################################################################
    # Analyze the beams
    ###########################################################################
    mainBeam.computation_stations()

    mainBeam.flexibility_analyze(uls_combos,patterns,off_patt)
    mainBeam.flexibility_analyze(basic_combos,patterns,off_patt)
    mainBeam.flexibility_analyze(sls_combos,patterns,off_patt)

    mainBeam.ULS_envelopes()
    mainBeam.SLS_envelopes()

    for load in mainBeam.Loads:
        if load.kind == "TRAP":
            print(load.w1)
            print(load.w2)
            print(load.a)
            print(load.b)
            print(load.L)

    if cantLeft is not None:
        cantLeft.computation_stations()

        cantLeft.flexibility_analyze(uls_combos,patterns,off_patt)
        cantLeft.flexibility_analyze(basic_combos,patterns,off_patt)
        cantLeft.flexibility_analyze(sls_combos,patterns,off_patt)

        cantLeft.ULS_envelopes()
        cantLeft.SLS_envelopes()

    if cantRight is not None:
        cantRight.computation_stations()

        cantRight.flexibility_analyze(uls_combos,patterns,off_patt)
        cantRight.flexibility_analyze(basic_combos,patterns,off_patt)
        cantRight.flexibility_analyze(sls_combos,patterns,off_patt)

        cantRight.ULS_envelopes()
        cantRight.SLS_envelopes()

    ###########################################################################
    # End Analyze the beams
    ###########################################################################

    return {"mainbeam": mainBeam, "cantleft": cantLeft, "cantright": cantRight}
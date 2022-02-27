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

import enum
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


def SimpleBeam(inputs, log=True):

    computation_log = []

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
        elif w1 == -1*w2:
            # if w1 and w2 are equal but opposite sign there will be a div/0
            # error in the centroid calcultion for the load, rather than rework
            # the load class catch it here and split it into two loads.
            c = b-a
            newba = c/2 + a
            Loads.append([type, w1, 0.0, a, newba, k])
            Loads.append([type, 0.0, w2, newba, b, k])

            # flip switch on applied loads type
            if k in applied_loads:
                if not applied_loads[k]:
                    applied_loads[k] = True
                    
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

    if log:
        computation_log.append("Raw Load Input :")

        for load in Loads:
            computation_log.append(f"{load}")

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
    
    elif inputs['combos'] == 1:
        uls_combos_bulk = LC.IBC2018_ULS(IBC_f1, IBC_f2, lateralReverse)
    else:
        uls_combos_bulk = []

    # User defined Ultimate Combinations
    user_uls_combos = []

    for i, userCombo in enumerate(inputs['uls']):
        userid = f'User_ULS{i+1}'

        loadFactors = {}
        pattern = []
        for j, factor in enumerate(userCombo):
            if factor == 0 or j == len(userCombo)-1:
                pass
            else:
                loadFactors[LoadKinds[j]] = factor
                pattern = userCombo[-1]
                
        if loadFactors == {}:
            pass
        else:
            user_uls_combos.append(LC.LoadCombo(userid, loadFactors,
                                       patterned=pattern, combo_type='ULS'))

    # User defined Service Combinations
    sls_combos = []

    for i, userCombo in enumerate(inputs['sls']):
        userid = f'S{i+1}'

        loadFactors = {}
        pattern = []
        for j, factor in enumerate(userCombo):
            if factor == 0 or j == len(userCombo)-1:
                pass
            else:
                loadFactors[LoadKinds[j]] = factor
                pattern = userCombo[-1]

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
    
    for combo in user_uls_combos:
        uls_combos.append(combo)

    # Trim out Basic Combos
    basic_combos = []
    for combo in basic_combos_bulk:
        test = []
        for kind in combo.principle_loads:
            test.append(applied_loads[kind])
        if any(test):
            basic_combos.append(combo)
    
    if log:
        computation_log.append("Load Combination Processing :")
        computation_log.append('Applied Load Type Key:')
        for k,v in applied_loads.items():
            computation_log.append(f'{k} : {v}')
        
        computation_log.append('IBC f1,f2:')
        computation_log.append(f"f1:{IBC_f1}")
        computation_log.append(f"f2:{IBC_f2}")

        computation_log.append(f'Lateral Reversal:{lateralReverse}')

        computation_log.append('Full ULS Combinations:')
        for combo in uls_combos_bulk:
            computation_log.append(combo.FormulaString())

        computation_log.append('Applied Reduced ULS Combinations:')
        for combo in uls_combos:
            computation_log.append(combo.FormulaString())

        computation_log.append('Full Basic Combinations:')
        for combo in basic_combos_bulk:
            computation_log.append(combo.FormulaString())

        computation_log.append('Applied Reduced Basic Combinations:')
        for combo in basic_combos:
            computation_log.append(combo.FormulaString())
        
        computation_log.append('Applied SLS Combinations:')
        for combo in sls_combos:
            computation_log.append(combo.FormulaString())

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

    # set the offPattern dictionary
    off_patt = {"L": inputs['offPat'][0],
                "Lr": inputs['offPat'][1],
                "S": inputs['offPat'][2],
                "R": inputs['offPat'][3], }

    if log:
        computation_log.append('Geometry:')
        computation_log.append(f'E: {E_ksi} ksi converted to E: {E_ksf} ksf')
        computation_log.append(f'Ixx: {I_in4} in4 converted to Ixx: {I_ft4} ft4')
        computation_log.append('Nodes:')
        for node in nodes:
            computation_log.append(f'Node:{node.userid} - Node #:{node.number} - ({node.x:4f},{node.y:4f})')
        
        computation_log.append(f"Left Overhang: {overhangLeft_ft} ft")
        computation_log.append(f"Right Overhang: {overhangRight_ft} ft")

        computation_log.append(f"Main span: {mainSpan_ft} ft")
        computation_log.append("Additional Supports @ :")
        for support in interiorSupports_ft:
            computation_log.append(f"local: {support} ft -- global: {support+n1.x} ft")
        computation_log.append(f'End Fixity: {endFixity}')

        computation_log.append(f'Number of Spans: {num_spans}')
        computation_log.append('Load Patterns:')

        if num_spans < 7:
            computation_log.append('Full Patterning')
        else:
            computation_log.append('ACI Reduced Patterning')

        for pattern in patterns:
            computation_log.append(f'{pattern}')
        
        computation_log.append('Off Pattern Factors:')
        for k,v in off_patt.items():
            computation_log.append(f'{k}: {v}')


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

    if log:
        computation_log.append("Process Loads to Analytical:")
        computation_log.append("global Spans:")
        for i,j in enumerate(globalSpans):
            computation_log.append(f"{j} ft -- ID: {spanIDs[i]}")

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

            print("globalspans:")
            print(globalSpans)

            # Since the load is applied over some finite length
            # step through each span and solve the parametric eqn
            # for the load length for t, if t is between 0 and 1
            # then all or a portion of the load applies in the span
            for i, span in enumerate(globalSpans):
                # span = a + t (b-a)
                # t < 0 then load starts after current span
                # t >= 1 then the whole load is before the span
                t = (span - a)/(b-a) # whoops need to validate b-a != 0

                # test 1
                if t < 0:
                    # load starts after span
                    pass

                # test 2
                elif i == 0 and t >= 0:
                    # entire load is in the first span

                    # test 2-1a
                    if t > 1:
                        # load entirely in the first span
                        
                        # test 2-1aa
                        if cantLeft is not None:
                            print("test 2-1aa -- w/cantLeft")
                            print(f"w1:{w1},w2:{w2},a:{a},b:{b},{kind},id:{spanIDs[i]}")
                            if log:
                                computation_log.append("test 2-1aa -- w/cantLeft")
                                computation_log.append(f"w1:{w1},w2:{w2},a:{a},b:{b},{kind},id:{spanIDs[i]}")
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
                        
                        #test 2-1ab
                        else:
                            print("test 2-1ab -- no cantLeft")
                            print(f"w1:{w1},w2:{w2},a:{a},b:{b},{kind},id:{spanIDs[i]}")
                            if log:
                                computation_log.append("test 2-1ab -- no cantLeft")
                                computation_log.append(f"w1:{w1},w2:{w2},a:{a},b:{b},{kind},id:{spanIDs[i]}")
                            # limitation of the app is you need a main span to have
                            # a right cantilever, and globalSpans includes the
                            # interior spans of the main span so we can apply
                            # the load to the whole first span and it will be on
                            # the mainbeam and in the mainbeams local coordinates.

                            mainbeamLoads.append(
                                ebl.trap(w1,w2,a,b,mainBeam.span,kind,spanIDs[i]))
                    
                    # test 2-1b
                    else:
                        # load extends beyond first span
                        # interpolate w2
                        wc = w1 + (t*(w2-w1))
                        c = span
                        
                        # test 2-1ba
                        if cantLeft is not None:
                            print("test 2-1ba -- w/ cantLeft")
                            print(f"w1:{w1},w2:{wc},a:{a},b:{c},{kind},id:{spanIDs[i]}")
                            if log:
                                computation_log.append("test 2-1ba -- w/ cantLeft")
                                computation_log.append(f"w1:{w1},w2:{wc},a:{a},b:{c},{kind},id:{spanIDs[i]}")
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
                        
                        # test 2-1bb
                        else:
                            print("test 2-1bb -- no cantLeft")
                            print(f"w1:{w1},w2:{wc},a:{a},b:{c},{kind},id:{spanIDs[i]}")

                            if log:
                                computation_log.append("test 2-1bb -- no cantLeft")
                                computation_log.append(f"w1:{w1},w2:{wc},a:{a},b:{c},{kind},id:{spanIDs[i]}")

                            # limitation of the app is you need a main span to have
                            # a right cantilever, and globalSpans includes the
                            # interior spans of the main span so we can apply
                            # the load to the whole first span and it will be on
                            # the mainbeam and in the mainbeams local coordinates.

                            if a == c:
                                print("test 2-1bb -- no cantLeft")
                                print("a=c, catch div/0")
                                pass
                            else:
                                mainbeamLoads.append(
                                    ebl.trap(w1,wc,a,c,mainBeam.span,kind,spanIDs[i]))

                # test 2-2
                elif span != globalSpans[-1] and t > 0:
                    # if we are not in the end span and we are not in the first
                    # span then we are at some intermediate span within the main
                    # span.

                    # determine t for the previous span
                    tp = (globalSpans[i-1]-a)/(b-a)

                    # tp < 0 load starts in the span
                    # tp >= 0 load starts at or prior to the span

                    # test 2-2a
                    if tp <= 0:
                        # the load starts in or at this span
                        # subtract the left support x from a to get
                        # a in the local system of the mainbeam
                        xa = a - mainBeam.node_i.x
                        
                        # determine if w2 needs to be truncated
                        
                        # test 2-2aa
                        if t <= 1:
                            # then then the load encompasses the span
                            # interpolate w2 and b
                            wc = w1 + (t*(w2-w1))
                            c = a + (t*(b-a))

                            # c is in the global system need to subtract the 
                            # left support x to get it to local
                            xc = c - mainBeam.node_i.x

                            print("test 2-2aa")
                            print(f"w1:{w1},w2:{wc},a:{xa},b:{xc},{kind},id:{spanIDs[i]}")

                            if log:
                                computation_log.append("test 2-2aa")
                                computation_log.append(f"w1:{w1},w2:{wc},a:{xa},b:{xc},{kind},id:{spanIDs[i]}")

                            mainbeamLoads.append(
                                ebl.trap(w1,wc,xa,xc,mainBeam.span,kind,spanIDs[i]))
                        
                        # test 2-2ab
                        else:
                            # other option is t > 1 which means the load ends
                            # in this span, and W2 does not need to be interpolated

                            # b is in the global system need to subtract the 
                            # left support x to get it to local
                            xb = b - mainBeam.node_i.x

                            print("test 2-2ab")
                            print(f"w1:{w1},w2:{w2},a:{xa},b:{xb},{kind},id:{spanIDs[i]}")

                            if log:
                                computation_log.append("test 2-2ab")
                                computation_log.append(f"w1:{w1},w2:{w2},a:{xa},b:{xb},{kind},id:{spanIDs[i]}")

                            mainbeamLoads.append(
                                ebl.trap(w1,w2,xa,xb,mainBeam.span,kind,spanIDs[i]))

                    # test 2-2b
                    else:
                        # the load started prior to this span
                        # interpolate w1
                        wc = w1 + (tp*(w2-w1))
                        # locally the load start point is the span start point
                        xc = globalSpans[i-1] - mainBeam.node_i.x

                        # test 2-2ba
                        if t<=1:
                            # then the load encompasses the span
                            # interpolate w2 and b
                            wd = w1 + (t*(w2-w1))
                            d = a + (t*(b-a))

                            xd = d - mainBeam.node_i.x
                            
                            print("test 2-2ba")
                            print(f"w1:{wc},w2:{wd},a:{xc},b:{xd},{kind},id:{spanIDs[i]}")

                            if log:
                                computation_log.append("test 2-2ba")
                                computation_log.append(f"w1:{wc},w2:{wd},a:{xc},b:{xd},{kind},id:{spanIDs[i]}")

                            mainbeamLoads.append(
                                ebl.trap(wc,wd,xc,xd,mainBeam.span,kind,spanIDs[i]))

                        # test 2-2bb
                        elif t>1 and tp>=1:
                            # Loads ends at the beginning of this span
                            print("test 2-2bb")
                            print("pass")
                            if log:
                                computation_log.append("test 2-2bb")
                                computation_log.append("pass")
                            pass

                        # test 2-2bc
                        else:
                            # other option is t>1 which means the load ends
                            # in this span, and W2 does not require interpolation

                            xb = b - mainBeam.node_i.x

                            print("test 2-2bc")
                            print(f"w1:{wc},w2:{w2},a:{xc},b:{xb},{kind},id:{spanIDs[i]}")

                            if log:
                                computation_log.append("test 2-2bc")
                                computation_log.append(f"w1: {wc}, w2: {w2}, a: {xc}, b: {xb}, {kind}, id: {spanIDs[i]}")

                            mainbeamLoads.append(
                                ebl.trap(wc,w2,xc,xb,mainBeam.span,kind,spanIDs[i]))

                # test 2-3
                elif span == globalSpans[-1] and t > 0:
                    # we are in the last span
                    # determine t for the previous span
                    tp = (globalSpans[i-1]-a)/(b-a)

                    # tp < 0 load starts in the span
                    # tp >= 0 load starts at or prior to the span

                    # test 2-3a
                    if tp <= 0:
                        # load starts at or in this span

                        # test 2-3aa
                        if cantRight is not None:
                            # a needs to be converted to the cantilever
                            # local system
                            xa = a - mainBeam.node_j.x

                            # assume the load end point was not allowed
                            # to go off the beam end
                            xb = b - mainBeam.node_j.x

                            print("test 2-3aa -- w/ cantRight")
                            print(f"w1:{w1},w2:{w2},a:{xa},b:{xb},{kind},id:{spanIDs[i]}")

                            if log:
                                computation_log.append("test 2-3aa -- w/ cantRight")
                                computation_log.append(f"w1:{w1},w2:{w2},a:{xa},b:{xb},{kind},id:{spanIDs[i]}")

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
                        # test 2-3ab
                        else:
                            # we are in the last span of the main beam
                            xa = a - mainBeam.node_i.x
                            xb = b - mainBeam.node_i.x

                            print("test 2-3ab -- no cantRight")
                            print(f"w1:{w1},w2:{w2},a:{xa},b:{xb},{kind},id:{spanIDs[i]}")

                            if log:
                                computation_log.append("test 2-3ab -- no cantRight")
                                computation_log.append(f"w1:{w1},w2:{w2},a:{xa},b:{xb},{kind},id:{spanIDs[i]}")

                            mainbeamLoads.append(
                                ebl.trap(w1,w2,xa,xb,mainBeam.span,kind,spanIDs[i]))
                    
                    # test 2-3b
                    else:
                        # Loaded started prior to this span
                        # interpolate w1
                        wc = w1 + (tp*(w2-w1))

                        # test 2-3ba
                        if cantRight is not None:
                            # locally the load start point is the span start point
                            xc = globalSpans[i-1] - mainBeam.node_j.x

                            # assume the load end point was not allowed
                            # to go off the beam end
                            xb = b - mainBeam.node_j.x

                            # test 2-3baa
                            if xc == xb:
                                print("test 2-3baa")
                                print("pass -- xc == xb")
                                if log:
                                    computation_log.append("test 2-3baa")
                                    computation_log.append("pass -- xc == xb")
                                pass
                            
                            # test 2-3bab
                            elif xb < xc:
                                print("test 2-3bab")
                                print("pass -- xb < xc, load not in this span")
                                if log:
                                    computation_log.append("test 2-3bab")
                                    computation_log.append("pass -- xb < xc, load not in this span")
                                pass
                            
                            # test 2-3bac
                            else:
                                print("test 2-3bac -- w/ cantRight")
                                print(f"w1:{wc},w2:{w2},a:{xc},b:{xb},{kind},id:{spanIDs[i]}")

                                if log:
                                    computation_log.append("test 2-3bac -- w/ cantRight")
                                    computation_log.append(f"w1:{wc},w2:{w2},a:{xc},b:{xb},{kind},id:{spanIDs[i]}")

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

                        # test 2-3bb
                        else:
                            # we are in the last beam span
                            xc = globalSpans[i-1] - mainBeam.node_i.x
                            xb = b - mainBeam.node_i.x

                            # one last check to see if we landed on a support
                            # test 2-3bba
                            if xc == xb:

                                print("test 2-3bba")
                                print("pass -- xc == xb")

                                if log:
                                    computation_log.append("test 2-3bba")
                                    computation_log.append("pass -- xc == xb")

                                pass
                            
                            # test 2-3bbb
                            elif xb < xc:
                                print("test 2-3bbb")
                                print("pass -- xb < xc, load not in this span")
                                if log:
                                    computation_log.append("test 2-3bbb")
                                    computation_log.append("pass -- xb < xc, load not in this span")
                                pass
                            # test 2-3bbc
                            else:

                                print("test 2-3bbc")
                                print(f"w1:{wc},w2:{w2},a:{xc},b:{xb},{kind},id:{spanIDs[i]}")

                                if log:
                                    computation_log.append("test 2-3bbc")
                                    computation_log.append(f"w1:{wc},w2:{w2},a:{xc},b:{xb},{kind},id:{spanIDs[i]}")

                                mainbeamLoads.append(
                                    ebl.trap(wc,w2,xc,xb,mainBeam.span,kind,spanIDs[i]))
                # test 2-4
                else:
                    print("test 2-4")
                    print("something wrong with load data")

                    if log:
                        computation_log.append("test 2-4")
                        computation_log.append("something wrong with load data")

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

    if cantLeft is not None:

        # need to correct the SLS and Basic starting slope to account
        # for the joint rotation
        cantLeftslopefrommain = mainBeam.slope_to_cant(cantLeft,True)

        cantLeft.addLoads(cantLeftslopefrommain)

        cantLeft.computation_stations()

        cantLeft.flexibility_analyze(uls_combos,patterns,off_patt)
        cantLeft.flexibility_analyze(basic_combos,patterns,off_patt)
        cantLeft.flexibility_analyze(sls_combos,patterns,off_patt)

        cantLeft.ULS_envelopes()
        cantLeft.SLS_envelopes()

    if cantRight is not None:

        # need to correct the SLS and Basic starting slope to account
        # for the joint rotation
        cantRightslopefrommain = mainBeam.slope_to_cant(cantRight,False)

        cantRight.addLoads(cantRightslopefrommain)

        cantRight.computation_stations()

        cantRight.flexibility_analyze(uls_combos,patterns,off_patt)
        cantRight.flexibility_analyze(basic_combos,patterns,off_patt)
        cantRight.flexibility_analyze(sls_combos,patterns,off_patt)

        cantRight.ULS_envelopes()
        cantRight.SLS_envelopes()

    ###########################################################################
    # End Analyze the beams
    ###########################################################################

    return {"mainbeam": mainBeam, "cantleft": cantLeft, "cantright": cantRight, "log": computation_log}
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

    ############################################################################
    # Loads Pre-Process
    ############################################################################

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

    ############################################################################
    # End Loads Pre-Process
    ############################################################################

    ############################################################################
    # Create and Process the Load Combinations
    ############################################################################

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

    ############################################################################
    # End of the Load Combination Processing
    ############################################################################

    ############################################################################
    # Begin Geometry
    ############################################################################

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

    print(off_patt)
    ############################################################################
    # End Geometry
    ############################################################################

    ############################################################################
    # Process the Loads to their analytical class
    ############################################################################

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

    print(mainSpans)
    print(globalSpans)
    print(spanIDs)

    cantLeftLoads = []
    mainbeamLoads = []
    cantRightLoads = []

    for load in Loads:

        type = load[0]
        kind = load[-1]

        if type == "POINT" or type == "MOMENT":
            p = load[1]
            a = load[2]
            # Get the index of the span start point
            # that is greater than a
            globalIndex = next(
                x for x, val in enumerate(globalSpans) if val > a)
            loadspanID = spanIDs[globalIndex]

            if cantLeft is not None and loadspanID == 1:
                if type == "POINT":
                    cantLeftLoads.append(ebl.cant_left_point(
                        p, a, cantLeft.span, 0, kind, loadspanID))
                else:
                    cantLeftLoads.append(ebl.cant_left_point_moment(
                        p, a, cantLeft.span, 0, kind, loadspanID))

            if cantRight is not None and loadspanID == spanIDs[-1]:
                # if this is the right cantilever we need to subtract out
                # the x coordinate of the left end of the beam from a
                # to give a in terms of the local length of the beam.
                xa = a - nodes[-2].x
                if type == "POINT":
                    cantRightLoads.append(ebl.cant_right_point(
                        p, xa, cantRight.span, 0, kind, loadspanID))
                else:
                    cantRightLoads.append(ebl.cant_right_point_moment(
                        p, xa, cantRight.span, 0, kind, loadspanID))

    ############################################################################
    # End Process the Loads to their analytical class
    ############################################################################

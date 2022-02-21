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

import analysis.ebloads as ebl
import numpy as np


def flexibility_solver(delta, reaction_points, L, fem, loadtype, span):

    #######################################################################################################
    #
    # Solve Simultaneous equation for internal reactions and fixed end moments knowing
    # deflection and end slopes of simple beam at support points:
    #
    # By compatibility for fixed ends initial and final slope should be 0, and deflection
    # at each interior support location should be 0.
    #
    # Function expects consistent units for values, should produce accurate results for
    # both metric and imperial units.
    #
    #[s0, sL, d1....di] = [M0,ML,p1....pi]*[eis0_M0, eis0_ML, eis0_p1......eis0_pi
    #                                       eisL_M0, eisL_ML, eisL_p1......eisL_pi
    #                                       eid_M0_p1,  eid_ML_p1, eid_p11.....eid_pi1
    #                                       eid_M0_pi,  eid_ML_pi, eid_p1i.....eid_pii]
    # Where:
    # s0 = slope at 0 ft, or left end of beam, calculated for the single span simply supported beam
    # sL = slope at L ft, or right end of beam, calculated for the single span simply supported beam
    # d1 = deflection at first interior support 1 location calculated for the single span simply supported beam
    # di = deflection at ith interior support i location calculated for the single span simply supported beam
    #
    # s and d are to be independant of E, modulus of elasticity, and I, moment of inertia, therefore
    # either need to divide by E*I or provide s and d in terms of E*I*s and E*I*d
    #
    # M0 = fixed end moment at 0 ft, or left end
    # Ml = fixed end moment at L ft, or right end
    # p1 = reaction at first interior support
    # pi = reaction at ith interior support
    #
    # eis0_M0 = slope coefficient for M0 at 0 ft, or left end
    # eis0_Ml = slope coefficient for ML at 0 ft, or left end
    # eis0_p1 = slope coefficient for first interior support at 0 ft, or left end
    # eis0_pi = slope coefficient for ith interior support at 0 ft, or left end
    #
    # eisL_M0 = slope coefficient for M0 at L ft, or right end
    # eisL_Ml = slope coefficient for ML at L ft, or right end
    # eisL_p1 = slope coefficient for first interior support at L ft, or right end
    # eisL_pi = slope coefficient for ith interior support at L ft, or right end
    #
    # eid_M0_p1 = deflection coefficient at first interior support for M0
    # eid_M0_p1 = deflection coefficient at first interior support for ML
    # eid_p11 = deflection coefficient at first interior support for first interior reaction
    # eid_pi1 = deflection coefficient at first interior support for ith interior reaction
    #
    # eid_M0_pi = deflection coefficient at ith interior support for M0
    # eid_M0_pi = deflection coefficient at ith interior support for ML
    # eid_p1i = deflection coefficient at ith interior support for first interior reaction
    # eid_pii = deflection coefficient at ith interior support for ith interior reaction
    #
    # Inputs:
    # delta = [eis0, eisL, eid1,...,eidi], list of deformation results for pin-pin beam from loading
    #   --note: deformation results must be in the order shown--
    # reaction_points = [p1,....,pi], list of locations of redundant interior supports
    # L = beam span
    # fem = [1,1], where a 1 signifies the location is fixed
    #
    # Assumptions:
    # 1. consistent units are used for the inputs
    # 2. the deformations entered are the actual deformations not
    #    the inverse ie not the restoring deformation.
    #
    #######################################################################################################

    # build the coefficient matrix rows and the deflection values
    coeff_matrix = []

    delta = [-1.0*x for x in delta]

    #Start Moment Component
    mo = ebl.point_moment(1,0,L,loadtype, span)
    ml = ebl.point_moment(1,L,L,loadtype, span)

    coeff_matrix.append([mo.eisx(0)*fem[0],ml.eisx(0)*fem[1]])
    coeff_matrix.append([mo.eisx(L)*fem[0],ml.eisx(L)*fem[1]])

    for support in reaction_points:
        a = support

        point_load = ebl.pl(1,a,L)

        coeff_row = []

        coeff_row.append(mo.eidx(a)*fem[0])
        coeff_row.append(ml.eidx(a)*fem[1])

        for point in reaction_points:

            x = point
            new_pl = ebl.pl(1,x,L)
            eid_p = new_pl.eidx(a)

            coeff_row.append(eid_p)

        coeff_matrix[0].append(point_load.eisx(0))
        coeff_matrix[1].append(point_load.eisx(L))

        coeff_matrix.append(coeff_row)

    d = np.array(delta)
    coeff = np.array(coeff_matrix)

    if fem == [0,1]:
        d = np.delete(d, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=1)

        reaction_points = [0] + reaction_points

    elif fem == [1,0]:
        d = np.delete(d, (1), axis=0)
        coeff = np.delete(coeff, (1), axis=0)
        coeff = np.delete(coeff, (1), axis=1)

        reaction_points = [0] + reaction_points

    elif fem == [0,0]:
        d = np.delete(d, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=1)

        d = np.delete(d, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=0)
        coeff = np.delete(coeff, (0), axis=1)
    else:
        reaction_points = [0,0] + reaction_points

    R = np.linalg.solve(coeff, d)

    # List of reactions defined as loads from class types in the ebloads.py file
    reactions_as_loads = []

    i = 0
    for reaction in R:
        if (fem == [1,0] or fem == [1,1]) and i == 0:
            m = reaction
            reactions_as_loads.append(ebl.point_moment(m,0,L, loadtype, span))

        elif fem == [0,1] and i == 0:
            m = reaction
            reactions_as_loads.append(ebl.point_moment(m,L,L,loadtype, span))

        elif fem == [1,1] and i == 1:
            m = reaction
            reactions_as_loads.append(ebl.point_moment(m,L,L,loadtype, span))

        else:
            p = reaction
            a = reaction_points[i]
            reactions_as_loads.append(ebl.pl(p,a,L,loadtype, span))

        i+=1

    return R, reactions_as_loads

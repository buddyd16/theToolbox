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
import numpy as np

def combine_piecewise_functions(Fa, Fb, LFa, LFb):
    '''
    Join two piecewise functions to create one piecewise function ecompassing
    the ranges and polynomials associated with each
    '''
    
    functions = [Fa,Fb]
    LF = [LFa, LFb]
    
    # Gather the ranges for each piece of the the two input functions
    ab = []
    for func in Fa:
        ab.append(func[1][0])
        ab.append(func[1][1])
    
    for func in Fb:
        ab.append(func[1][0])
        ab.append(func[1][1])

    ab = list(set(ab))
    ab.sort()

    f_out = []

    for i, j in enumerate(ab):
        if i == 0:
            piece_range = [0, j]
        else:
            piece_range = [ab[i-1], j]

        if piece_range == [0, 0]:
            pass
        else:
            f = []

            for i,func in enumerate(functions):

                for piece in func:

                    if piece[1][0] < piece_range[1] and piece[1][1] >= piece_range[1]:
                            eq_len_delta = len(piece[0]) - len(f) # difference in number of coefficients

                            if eq_len_delta > 0:
                                f.extend([0]*eq_len_delta)
                            elif eq_len_delta < 0:
                                piece[0].extend([0]*abs(eq_len_delta))
                            else:
                                pass

                            f = [j*LF[i] + k for j,k in zip(piece[0], f)]
                    else:
                        pass

            f_out.append([f,piece_range])

    return f_out


def poly_eval(c_list,x):
    '''
    evaluate a polynomial defined by a list of coeff. in ascending order
    C0 + C1x + C2x^2 + ... + Cnx^n = [C0,C1,C2,...,Cn]
    '''
    i = 0
    res=0
    if all(c == 0 for c in c_list):
        pass
    else:
        for c in c_list:
            res = res + c*math.pow(x,i)
            i+=1

    return res


def eval_piece_function(piece_function, x):
    '''
    Given a peicewise function and an x evaluate the results
    '''

    if piece_function == []:
        res = 0
    else:
        for line in piece_function:
            if line[1][0] == 0 and x == 0:
                res = poly_eval(line[0], x)
            if line[1][0] < x <= line[1][1]:
                res = poly_eval(line[0], x)
            else:
                pass

    return res


def roots_piecewise_function(piece_function):
    '''
    Given a piecewise function return a list
    of the location of zeros or sign change
    '''

    zero_loc = []
    i=0
    for line in piece_function:

        if len(line[0]) == 1 and i==0:
            pass # If function is a value then there is no chance for a sign change

        else:
            a = poly_eval(line[0], line[1][0]+0.0001) # value at start of bounds
            b = poly_eval(line[0], line[1][1]-0.0001) # value at end of bounds

            if a==0:
                zero_loc.append(line[1][0])

            elif b==0:
                zero_loc.append(line[1][1])

            else:
                # if signs are the the same a/b will result in a positive value
                coeff = line[0][::-1]
                c = np.roots(coeff)
                # Some real solutions may contain a very small imaginary part
                # account for this with a tolerance on the imaginary
                # part of 1e-5
                c = c.real[abs(c.imag)<1e-5]
                for root in c:
                    # We only want roots that are with the piece range
                    if line[1][0] < root <= line[1][1]:
                        zero_loc.append(root)
                    else:
                        pass

            if i==0:
                pass
            else:
                d = poly_eval(piece_function[i-1][0], line[1][0]-0.0001) # value at end of previous bounds

                if d == 0:
                    pass
                elif a/d < 0:
                    zero_loc.append(line[1][0])
                else:
                    pass
        i+=1

    zero_loc = sorted(set(zero_loc))

    return zero_loc
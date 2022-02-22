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
import itertools

class LoadCombo():
    
    '''
    Class for Load Combinations
    '''
    
    def __init__(self,name,factors={},principle_loads=[],patterned=False,combo_type=None):
        """
        
        Parameters
        ----------
        name : String
            User defined name for the load combinations.
        factors : TYPE, optional
            Dictionary of Load Factors with Keys set to the load kind string
            and values set to the load factor.
            ie. {"D":1.4,"F":1.4}
        principle_loads : TYPE, optional
            A list of the principle load kinds governing the load combination.
            This list will be used to skip redundant combinations or combinations
            where the member has no loads of the principal kind applied.
            The default is [].
        patterned : Boolean, optional
            A boolean to indicate whether the combination should consider load
            patterning. The default is False.
        combo_type : String, optional
            A string to indicate whethe the combination is a design combination
            or a service combination. For beam analysis design combinations will
            limit computations to shear and moment only while service combinations
            will result in full computation of shear, moment, slope and deflection.
            design = "ULS"
            service = "SLS"
            Anything other than "SLS" will be treated as a design designation.
            The default is None.

        Returns
        -------
        None.

        """

        self.name = name
        self.factors = factors
        self.principle_loads = principle_loads
        self.patterned = patterned
        self.combo_type = combo_type

    def __str__(self):
        '''
        Determine the output when print() is called on a load combo
        '''
        print(f'Combo: {self.name}')
        print(f'Type: {self.combo_type}')
        print(f'Pattern: {self.patterned}')

        key_loads = ''

        for key_load in self.principle_loads:
            key_loads += f'{key_load}'

        print(f'Principle Loads: {key_loads}')

        combo_formula = ''
        i = 0

        for Load_type, factor in self.factors.items():

            if i == 0:
                combo_formula += f'{factor}{Load_type}'
            else:
                combo_formula += f'+{factor}{Load_type}'
            i += 1

        return combo_formula

    def AddLoadCase(self, case_name, factor):
        '''
        Adds a load case with its associated load factor
        '''

        self.factors[case_name] = factor
    
    def DeleteLoadCase(self, case_name):
        '''
        Deletes a load case with its associated load factor
        '''

        del self.factors[case_name]

def Full_LoadPatterns(num_spans):
    patterns = []
    n = num_spans
    for r in range(n):
       for item in itertools.combinations(range(n), r):
           check = [1]*n
           for i in item:
               check[i] = 0
           patterns.append(check)
    return patterns

def ACI_LoadPatterns(n, byspan=True):
    pat1 = [1 for i in range(1,n+1)] # all spans loaded
    pat2 = [1 if i % 2 == 0 else 0 for i in range(1,n+1)] # even spans loaded
    pat3 = [0 if i % 2 == 0 else 1 for i in range(1,n+1)] # odd spans loaded

    count = 0
    pat4 = []
    pat5 = []
    pat6 = []
    for i in range(1,n+1):

        if count<=1:
            if count == 0:
                pat4.append(1)
                pat5.append(0)
                pat6.append(1)
            else:
                pat4.append(1)
                pat5.append(1)
                pat6.append(0)
            count+=1
        else:
            pat4.append(0)
            pat5.append(1)
            pat6.append(1)
            count=0
    
    if n==1:
        patterns = [pat1]
        
    elif n==2:
        patterns = [pat1,pat2,pat3]
    
    elif n==3:
        patterns = [pat1,pat2,pat3,pat4,pat5]
        
    else:
        patterns = [pat1,pat2,pat3,pat4,pat5,pat6]
    
    if byspan == True:
        patterns_transpose = list(map(list, zip(*patterns)))

        return patterns_transpose
    else:
        return patterns
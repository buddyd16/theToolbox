'''
BSD 3-Clause License
Copyright (c) 2019-2022, Donald N. Bockoven III
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



class aisc_15th_database:
    def __init__(self):
        
        ## BUILD SHAPE DICTIONARY AND ATTRIBUTE LISTS
        ## NOTE THE STANDARD DATABADE PROVIDED BY AISC NEEDS TO BE CLEANED UP
        ## ALL - FIELDS NEED TO BE REPLACED BY 0's
        
        file = open('steel/static/aisc_shapes_database_v15.0.csv','r')
        
        data_raw = file.readlines()
        
        file.close()
        
        file = open('steel/static/aisc_v15_units.csv','r')
        units_raw = file.readlines()
        file.close()
        
        file = open('steel/static/aisc_v15_defs.csv','r')
        defs_raw = file.readlines()
        file.close()
        
        self.units = units_raw[0].split(',')
        self.units[-1] = self.units[-1].rstrip('\n')
        
        self.definitions = []
        self.defs_only = ['']
        for prop_def in defs_raw:
            prop_def = prop_def.split(',')
            prop_def[-1] = prop_def[-1].rstrip('\n')
            self.definitions.append(prop_def)
            self.defs_only.append(prop_def[1])
        
        self.labels = data_raw[0].split(',')
        self.labels[-1] = self.labels[-1].rstrip('\n')
        
        self.shapes = []
        self.shape_types = []
        
        for shape in data_raw[1:]:
            shape = shape.split(',')
            shape[-1] = shape[-1].rstrip('\n')
            if shape[0] == 'HSS':
                if float(shape[10]) > 0:
                    shape[0] = 'HSS-RND'
                elif shape[8] == shape[13]:
                    shape[0] = 'HSS-SQR'
                else:
                    shape[0] = 'HSS-RECT'
            else:
                pass
            
            self.shapes.append(shape)
            self.shape_types.append(shape[0])
        
        self.shape_types = list(set(self.shape_types))
        
    def WF(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []
        
        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []
        
        for shape in self.shapes:
            if shape[0] == 'W':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):

                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass
                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
    
    def PIPE(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []
        
        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'PIPE':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def C(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'C':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary

    def HSS_RND(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'HSS-RND':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary

    def MC(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'MC':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary

    def HSS_RECT(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'HSS-RECT':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def HP(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'HP':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def M(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'M':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def L(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'L':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def ST(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'ST':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def HSS_SQR(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'HSS-SQR':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def MT(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'MT':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def S(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'S':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def WT(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == 'WT':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
    def LL(self, filter=[], filter2=[]):
        shape_selection_list = []
        filtered_shape_list = []
        dictionary = []

        if filter != []:
            try:
                filterpropindex = self.labels[0:83].index(filter[0])
                filter_start = filter[1]
                filter_end = filter[2]
            except ValueError:
                filter = []

        if filter2 != []:
            try:
                filterpropindex2 = self.labels[0:83].index(filter2[0])
                filter_start2 = filter2[1]
                filter_end2 = filter2[2]
            except ValueError:
                filter2 = []

        for shape in self.shapes:
            if shape[0] == '2L':
                if filter == []:
                    shape_selection_list.append(shape[2])
                    filtered_shape_list.append(shape)

                    dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                elif (float(shape[filterpropindex]) >= filter_start and float(shape[filterpropindex]) <= filter_end):
                    if filter2 == []:
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))

                    elif (float(shape[filterpropindex2]) >= filter_start2 and float(shape[filterpropindex2]) <= filter_end2):
                        shape_selection_list.append(shape[2])
                        filtered_shape_list.append(shape)

                        dictionary.append(dict(zip(self.labels[0:83],zip(shape[0:83],self.units[0:83],self.defs_only))))
                    else:
                        pass

                else:
                    pass
            else:
                pass
        
        return shape_selection_list,filtered_shape_list,dictionary
        
db = aisc_15th_database()

defs = db.definitions

sections = db.shapes

labels = db.labels
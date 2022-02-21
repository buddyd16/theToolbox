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

class Node2D():
    '''
    class reprsenting the nodes of the structure in 2D x,y plane or R2
    '''

    def __init__(self, x, y, userid, number):
        '''
        x: float        x-coordinate of node
        y: float        y-cootdinate of node
        userid: string  User assigned name for the node
        number: int     User/Program assigned node number
        '''

        # Location in space
        self.x = x
        self.y = y

        # Indetifiers
        self.userid = userid
        self.number = number

        # Support condition initialized to all released
        # [tx,ty,rz]
        self.support = [0, 0, 0]

        # Nodal Loads
        # [Fx, Fy, Mz]
        self.loads = [0, 0, 0]

        # Nodal Displacements
        # [x, y, rz]
        self.displacements = [0, 0, 0]

    def __str__(self):
        '''
        define what will display when print() is called on a node object
        '''
        print(f'Node: {self.userid}')
        print(f'Node #: {self.number}')
        print(f'x: {self.x:4f}')
        print(f'y: {self.y:4f}')
        return f'Restraint: {self.support}'

    def supports(self, restraints):
        '''
        update the support conditions

        restraints: [int,int,int]   restraint condition
                                    1 = restrained
                                    0 = unrestrained
                    [tx,ty,rz]
        '''

        self.support = restraints

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

from __future__ import division
import math


def coordinate_rotation(x, y, xo, yo, angle):

    theta = math.radians(angle)

    x_t = (x-xo)*math.cos(theta)+(y-yo)*math.sin(theta)
    y_t = -1.0*(x-xo)*math.sin(theta)+(y-yo)*math.cos(theta)

    x_t = x_t+xo
    y_t = y_t+yo

    return [x_t, y_t]


class Section:

    def __init__(self, x, y, solid=True, n=1, E=1, Fy=1):
        '''
        A section defined by (x,y) vertices

        the vertices should for a closed polygon.
        initialization will check is first and last coordinate are equal
        and if not will add an additional vertex equal to the first

        Inputs:

        x = a list of x coordinate values
        y = a list of y coordinate values

        Assumptions:

        x and y are of consistent units
        x and y form a closed polygon with no segment overlaps

        If solid = 1 then the coordinates will be ordered so the signed area
        is positive

        n = property multiplier
        '''

        self.output = []
        self.output_strings = []

        self.E = E
        self.Fy = Fy

        # check if a closed polygon is formed from the coordinates
        # if not add another x and y coordinate equal to the firts
        # coordinate x and y

        self.warnings = ''
        if x[0] == x[-1] and y[0] == y[-1]:
            pass
        else:
            x.append(x[0])
            y.append(y[0])

            self.warnings = self.warnings + '**User Verify** Shape was not closed, program attempted to close it.\p'

        # check the signed area of the coordinates, should be positive
        # for a solid shape. If not reverse the coordinate order

        self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
        self.area = self.area*n
        
        if self.area < 0 and solid == True:
            x.reverse()
            y.reverse()
            self.warnings = self.warnings + '**User Verify** Coordinate order reversed to make signed area positive for a solid.\n'
            
            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
            self.area = self.area*n
            
        elif self.area > 0 and solid is False:
            x.reverse()
            y.reverse()
            self.warnings = self.warnings + '**User Verify** Coordinate order reversed to make signed area negative for a void.\n'
            
            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
            self.area = self.area*n
            
        elif self.area == 0:
            self.warnings = self.warnings + '**User Verify** Area = 0 - verify defined shape has no overlapping segments.\n'
            
        else:
            pass
        
        self.x = [i for i in x]
        self.y = [j for j in y]
        self.n = n
        
        if self.area == 0:
            pass
        else:
            self.calc_props()

    def change_n(self,n):
            self.n = n
            self.calc_props()
            
    def calc_props(self):
            x = self.x
            y = self.y
            n = self.n
            
            
            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
            self.area = self.area*n
            
            self.output.append(self.area)
            self.output_strings.append('Area')

            # properties about the global x and y axis
            
            self.cx = sum([(x[i]+x[i+1])*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(6*self.area)
            self.cx = self.cx*n
            self.output.append(self.cx)
            self.output_strings.append('Cx')
            self.cy = sum([(y[i]+y[i+1])*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(6*self.area)
            self.cy = self.cy*n
            self.output.append(self.cy)
            self.output_strings.append('Cy')
            self.output.append('---')
            self.output_strings.append('Global Axis:')           
            self.Ix = sum([((y[i]*y[i])+(y[i]*y[i+1])+(y[i+1]*y[i+1]))*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(12.0)
            self.Ix = self.Ix*n
            self.output.append(self.Ix)
            self.output_strings.append('Ix')
            self.Iy = sum([((x[i]*x[i])+(x[i]*x[i+1])+(x[i+1]*x[i+1]))*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(12.0)
            self.Iy = self.Iy*n
            self.output.append(self.Iy)
            self.output_strings.append('Iy')
            self.Ixy = sum([((x[i]*y[i+1])+(2*x[i]*y[i])+(2*x[i+1]*y[i+1])+(x[i+1]*y[i]))*(x[i]*y[i+1]-x[i+1]*y[i]) for i in range(len(x[:-1]))])/(24.0)
            self.Ixy = self.Ixy*n
            self.output.append(self.Ixy)
            self.output_strings.append('Ixy')
            self.Jz = self.Ix + self.Iy
            self.output.append(self.Jz)
            self.output_strings.append('Jz')
            self.sx_top = self.Ix / abs(max(y) - self.cy)
            self.output.append(self.sx_top)
            self.output_strings.append('Sx,top')
            self.sx_bottom = self.Ix / abs(min(y) - self.cy)
            self.output.append(self.sx_bottom)
            self.output_strings.append('Sx,botom')
            self.sy_right = self.Iy / abs(max(x) - self.cx)
            self.output.append(self.sy_right)
            self.output_strings.append('Sy,right')
            self.sy_left = self.Iy / abs(min(x) - self.cx)
            self.output.append(self.sy_left)
            self.output_strings.append('Sy,left')
            
            self.rx = math.sqrt(self.Ix/self.area)
            self.output.append(self.rx)
            self.output_strings.append('rx')
            self.ry = math.sqrt(self.Iy/self.area)
            self.output.append(self.ry)
            self.output_strings.append('ry')
            self.rz = math.sqrt(self.Jz/self.area)
            self.output.append(self.rz)
            self.output_strings.append('rz')
            
            # properties about the cross section centroidal x and y axis
            # parallel axis theorem Ix = Ixx + A*d^2
            # therefore to go from the global axis to the local
            # Ixx = Ix - A*d^2
            self.output.append('--')
            self.output_strings.append('Shape Centroidal Axis:')
            self.Ixx = self.Ix - (self.area*self.cy*self.cy)
            self.output.append(self.Ixx)
            self.output_strings.append('Ixx')
            self.Iyy = self.Iy - (self.area*self.cx*self.cx)
            self.output.append(self.Iyy)
            self.output_strings.append('Iyy')
            self.Ixxyy = self.Ixy - (self.area*self.cx*self.cy)
            self.output.append(self.Ixxyy)
            self.output_strings.append('Ixxyy')
            self.Jzz = self.Ixx + self.Iyy
            self.output.append(self.Jzz)
            self.output_strings.append('Jzz')
            self.sxx_top = self.Ixx / abs(max(y) - self.cy)
            self.output.append(self.sxx_top)
            self.output_strings.append('Sxx,top')
            self.sxx_bottom = self.Ixx / abs(min(y) - self.cy)
            self.output.append(self.sxx_bottom)
            self.output_strings.append('Sxx,bottom')
            self.syy_right = self.Iyy / abs(max(x) - self.cx)
            self.output.append(self.syy_right)
            self.output_strings.append('Syy,right')
            self.syy_left = self.Iyy / abs(min(x) - self.cx)
            self.output.append(self.syy_left)
            self.output_strings.append('Syy,left')
            
            self.rxx = math.sqrt(self.Ixx/self.area)
            self.output.append(self.rxx)
            self.output_strings.append('rxx')
            self.ryy = math.sqrt(self.Iyy/self.area)
            self.output.append(self.ryy)
            self.output_strings.append('ryy')
            self.rzz = math.sqrt(self.Jzz/self.area)
            self.output.append(self.rzz)
            self.output_strings.append('rzz')
            
            # Cross section principal Axis
            
            two_theta = math.atan2((-1*2.0*self.Ixxyy),(1E-16+(self.Ixx - self.Iyy)))
            A = (self.Ixx+self.Iyy)/2.0
            B = (self.Ixx-self.Iyy)/2.0
            I1 = A+math.sqrt((B*B)+(self.Ixxyy*self.Ixxyy))
            I2 = A-math.sqrt((B*B)+(self.Ixxyy*self.Ixxyy))
            
            self.output.append('--')
            self.output_strings.append('Shape Principal Axis:')
            self.Iuu = A+(B*math.cos(two_theta))-(self.Ixxyy*math.sin(two_theta))
            self.output.append(self.Iuu)
            self.output_strings.append('Iuu')
            self.Ivv = A-(B*math.cos(two_theta))+(self.Ixxyy*math.sin(two_theta))
            self.output.append(self.Ivv)
            self.output_strings.append('Ivv')
            self.Iuuvv = (B*math.sin(two_theta))+(self.Ixxyy*math.cos(two_theta))
            self.output.append(self.Iuuvv)
            self.output_strings.append('Iuuvv')
            
            if (I1-1E-10)<=self.Iuu and (I1+1E-10)>=self.Iuu:
                self.theta1 = math.degrees(two_theta/2.0)
                self.theta2 = self.theta1 + 90.0
            else:
                self.theta2 = math.degrees(two_theta/2.0)
                self.theta1 = self.theta2 + 90.0
            
            self.output.append(self.theta1)
            self.output_strings.append('Theta1,u')
            self.output.append(self.theta2)
            self.output_strings.append('Theta2,v')
            
            # Create coordinates for the XX,YY,UU,VV axis lines
            
            self.xx_axis=[min(x)-1,self.cy,max(x)+1,self.cy]
            self.yy_axis=[self.cx,min(y)-1,self.cx,max(y)+1]
            
            # UU axis coordinates
            
            u1 = coordinate_rotation(self.xx_axis[0],self.xx_axis[1],self.cx,self.cy,self.theta1)
            u2 = coordinate_rotation(self.xx_axis[2],self.xx_axis[3],self.cx,self.cy,self.theta1)
            
            self.uu_axis = [u1[0],u1[1],u2[0],u2[1]]
            
            # VV axis coordinates
            v1 = coordinate_rotation(self.xx_axis[0],self.xx_axis[1],self.cx,self.cy,self.theta2)
            v2 = coordinate_rotation(self.xx_axis[2],self.xx_axis[3],self.cx,self.cy,self.theta2)
            
            self.vv_axis = [v1[0],v1[1],v2[0],v2[1]]

    def calc_s_at_vertices(self):
        sx = []
        sy = []

        for y in shape.y:
            if y == 0:
                y=0.00000000000001
            else:
                pass
            
            sx.append(self.Ixx / abs(y - self.cy))
            
        for x in shape.x:
            if x == 0:
                x=0.00000000000001
            else:
                pass
            
            sy.append(self.Iyy / abs(x - self.cx))
        
        return sx,sy
            
    def parallel_axis_theorem(self, x, y):
        '''
        given a new global x,y coordinate for a new
        set of x, y axis return the associated Ix, Iy, and Ixy
        '''
        if self.area == 0:
            return [0,0,0]
        else:
            dx = self.cx - x
            dy = self.cy - y
            
            Ix = self.Ixx + (self.area*dy*dy)
            Iy = self.Iyy + (self.area*dx*dx)
            Ixy = self.Ixxyy + (self.area*dx*dy)
            
            return [Ix,Iy,Ixy]
    
    def transformed_vertices(self, xo, yo, angle):
        '''
        given an angle in degrees
        and coordinate to translate about
        return the transformed values of the shape vertices       
        '''
        theta = math.radians(angle)
        
        x_t = [(x-xo)*math.cos(theta)+(y-yo)*math.sin(theta) for x,y in zip(self.x, self.y)]
        y_t = [-1.0*(x-xo)*math.sin(theta)+(y-yo)*math.cos(theta) for x,y in zip(self.x, self.y)]
        
        x_t = [i+xo for i in x_t]
        y_t = [j+yo for j in y_t]
        
        self.x = x_t
        self.y = y_t
        
        self.calc_props()
        
        return [x_t, y_t]
    
    def translate_vertices(self, xo, yo):
        '''
        give an x and y translation
        shift the shape vertices by the x and y amount
        '''
        x_t = [x+xo for x in self.x]
        y_t = [y+yo for y in self.y]
        
        self.x = x_t
        self.y = y_t
        
        self.calc_props()
        
        return [x_t, y_t]
        
    def transformed_properties(self, x, y, angle):
        '''
        given a new global x,y coordinate for a new
        set of x, y axis and the axis angle. Return full set of transformed properties
        at the new axis
        
        input angle as degrees
        '''
        if self.area == 0:
            return [0,0,0,0,0,0,0]
        
        else:
            Ix, Iy, Ixy = self.parallel_axis_theorem(x,y)
            
            two_theta = 2*math.radians(angle)
            # I on principle Axis
            
            temp = (Ix+Iy)/2.0
            temp2 = (Ix-Iy)/2.0
            
            Iu = temp + temp2*math.cos(two_theta) - Ixy*math.sin(two_theta)
            Iv = temp - temp2*math.cos(two_theta) + Ixy*math.sin(two_theta)
            Iuv = temp2*math.sin(two_theta) + Ixy*math.cos(two_theta)
    
            Jw = Iu + Iv
            
            ru = math.sqrt(Iu/self.area)
            rv = math.sqrt(Iv/self.area)
            rw = math.sqrt(Jw/self.area)
            
            trans_coords = self.transformed_vertices(angle)
            
            return [Iu,Iv,Iuv,Jw,ru,rv,rw,trans_coords]
        
class Composite_Section:

    def __init__(self):

        self.sections = []
    
    def add_section(self,section):
        
        self.sections.append(section)
    
    def remove_section(self,section_index):

        self.sections.pop(section_index)
    
    def calculate_properties(self):

        # determine the global centroid location and total composite area
        # cx = sum A*dx / sum A
        # cy = sum A*dy / sum A
        # dx = section cx
        # dy = section cy
        # A = section area
        
        self.output = []
        self.output_strings = []    
        
        self.area = sum([section.area for section in self.sections])
        
        self.output.append(self.area)
        self.output_strings.append('Area')
        
        sum_A_dx = sum([section.area*section.cx for section in self.sections])
        sum_A_dy = sum([section.area*section.cy for section in self.sections])
        
        self.cx = sum_A_dx / self.area
        
        self.output.append(self.cx)
        self.output_strings.append('cx')
        
        self.cy = sum_A_dy / self.area
        
        self.output.append(self.cy)
        self.output_strings.append('cy')
        
        self.output.append('--')
        self.output_strings.append('Shape Centroidal Axis:')
        
        # determine moment of inertias about the centroid coordinates
        
        self.Ix = sum([section.parallel_axis_theorem(self.cx, self.cy)[0] for section in self.sections])

        self.output.append(self.Ix)
        self.output_strings.append('Ix')
        
        self.Iy = sum([section.parallel_axis_theorem(self.cx, self.cy)[1] for section in self.sections])

        self.output.append(self.Iy)
        self.output_strings.append('Iy')
        
        self.Ixy = sum([section.parallel_axis_theorem(self.cx, self.cy)[2] for section in self.sections])

        self.output.append(self.Ixy)
        self.output_strings.append('Ixy')
        
        self.Jz = self.Ix + self.Iy
        
        self.output.append(self.Jz)
        self.output_strings.append('Jz')
        
        # radii of gyration - centroidal axis
        self.rx = math.sqrt(self.Ix/self.area)
        self.output.append(self.rx)
        self.output_strings.append('rx')
        self.ry = math.sqrt(self.Iy/self.area)
        self.output.append(self.ry)
        self.output_strings.append('ry')
        self.rz = math.sqrt(self.Jz/self.area)
        self.output.append(self.rz)
        self.output_strings.append('rz')
        
        # composite section principal Axis
        
        two_theta = math.atan2((-1*2.0*self.Ixxyy),(1E-16+(self.Ixx - self.Iyy)))
        A = (self.Ixx+self.Iyy)/2.0
        B = (self.Ixx-self.Iyy)/2.0
        I1 = A+math.sqrt((B*B)+(self.Ixxyy*self.Ixxyy))
        I2 = A-math.sqrt((B*B)+(self.Ixxyy*self.Ixxyy))
        
        self.output.append('--')
        self.output_strings.append('Shape Principal Axis:')
        self.Iuu = A+(B*math.cos(two_theta))-(self.Ixxyy*math.sin(two_theta))
        self.output.append(self.Iuu)
        self.output_strings.append('Iuu')
        self.Ivv = A-(B*math.cos(two_theta))+(self.Ixxyy*math.sin(two_theta))
        self.output.append(self.Ivv)
        self.output_strings.append('Ivv')
        self.Iuuvv = (B*math.sin(two_theta))+(self.Ixxyy*math.cos(two_theta))
        self.output.append(self.Iuuvv)
        self.output_strings.append('Iuuvv')
        
        if (I1-1E-10)<=self.Iuu and (I1+1E-10)>=self.Iuu:
            self.theta1 = math.degrees(two_theta/2.0)
            self.theta2 = self.theta1 + 90.0
        else:
            self.theta2 = math.degrees(two_theta/2.0)
            self.theta1 = self.theta2 + 90.0
        
        self.output.append(self.theta1)
        self.output_strings.append('Theta1,u')
        self.output.append(self.theta2)
        self.output_strings.append('Theta2,v')
        
        # Create coordinates for the XX,YY,UU,VV axis lines
        
        self.xx_axis=[min([section.x for section in self.sections])-1,self.cy,max([section.x for section in self.sections])+1,self.cy]
        self.yy_axis=[self.cx,min([section.y for section in self.sections])-1,self.cx,max([section.y for section in self.sections])+1]
        
        # UU axis coordinates
        
        u1 = coordinate_rotation(self.xx_axis[0],self.xx_axis[1],self.cx,self.cy,self.theta1)
        u2 = coordinate_rotation(self.xx_axis[2],self.xx_axis[3],self.cx,self.cy,self.theta1)
        
        self.uu_axis = [u1[0],u1[1],u2[0],u2[1]]
        
        # VV axis coordinates
        v1 = coordinate_rotation(self.xx_axis[0],self.xx_axis[1],self.cx,self.cy,self.theta2)
        v2 = coordinate_rotation(self.xx_axis[2],self.xx_axis[3],self.cx,self.cy,self.theta2)
        
        self.vv_axis = [v1[0],v1[1],v2[0],v2[1]]

def circle_coordinates(x,y,r,start,end):
    '''
    given a center point x,y
    and a radius
    return the x,y coordinate list for a circle
    '''
    
    x_out = []
    y_out = []
    
    for a in range(start,end+1):
        x0 = r*math.cos(math.radians(a))
        y0 = r*math.sin(math.radians(a))
        
        x_out.append(x0+x)
        y_out.append(y0+y)
    
    return [x_out,y_out]

def line_x_at_y(x1,y1,x2,y2,at_y):
    '''
    given two points and a y coordinate
    return the corresponding x coordinate
    '''
    if x2 == x1:
        x_out = x1
    
    else:
        m = (y2-y1) / (x2-x1)
        
        # y = mx + b
        # b = y - mx
        b = y1 - (m*x1)
        
        # y = mx+b
        # x = y-b / m
        if m == 0:
            x_out = 0
        else:
            x_out = (at_y - b) / m
    
    return x_out

def dist_btwn_point_and_plane(point, xy, plane='H'):
    '''
    given a point as a list = [x,y]
    a plane elevation/location
    a plane orientation
    H = horizontal
    V = vertical
    
    return if the the point is in front, behind, or on
    the plane
    '''
    
    # General tolerance
    tol = 1E-16
    if plane=='H':
        dist = point[1] - xy
        
        if dist > tol:
            return 'over'
        elif dist < tol:
            return 'under'
        else:
            return 'on'
    
    elif plane == 'V':
        dist = point[0] - xy
        
        if dist > tol:
            return 'left'
        elif dist < tol:
            return 'right'
        else:
            return 'on'    

def split_shape_above_horizontal_line(shape, line_y, solid=True, n=1):
    
    '''
    given a shape and horizontal line y value
    return all the sub shapes above the line
    
    assumption:
        shape has been rotated to align with the horizontal
    '''
    # new shapes above
    sub_shapes = []
    
    if max(shape.y) < line_y:
        pass
    
    elif min(shape.y) > line_y:
        x = [i for i in shape.x]
        y = [j for j in shape.y]
        sub = Section(x,y,solid,n)
        
        sub_shapes.append(sub)        
    else:    
             
        xy = [[x,y] for x,y in zip(shape.x,shape.y)]
        
        list_above = []
        list_below = []
        
        i=0
        for point in xy:
            if i == len(xy)-1:
                pass
            else:
                p1 = point
                p2 = xy[i+1]
                
                p1_test = dist_btwn_point_and_plane(p1, line_y,'H')
                p2_test = dist_btwn_point_and_plane(p2, line_y,'H')
                
                if p1_test=='over' and p2_test=='over':
                    list_above.append(p2)
                
                elif p1_test=='on' and p2_test=='over':
                    list_above.append(p2)
                    
                elif p1_test=='under' and p2_test=='over':
                    x_int = line_x_at_y(p1[0],p1[1],p2[0],p2[1],line_y)
                    list_above.append([x_int,line_y])
                    list_above.append(p2)
                    list_below.append(p1)
                    list_below.append([x_int,line_y])
                    
                elif p1_test=='over' and p2_test=='on':
                    list_above.append(p2)
                
                elif p1_test=='on' and p2_test=='on':
                    list_above.append(p2)
                    
                elif p1_test=='under' and p2_test=='on':
                    list_above.append(p2)
                    list_below.append(p2)
                
                elif p1_test=='over' and p2_test=='under':
                    x_int = line_x_at_y(p1[0],p1[1],p2[0],p2[1],line_y)
                    list_above.append([x_int,line_y])
                    list_below.append([x_int,line_y])
                    list_below.append(p2)
                
                elif p1_test=='on' and p2_test=='under':
                    list_below.append(p1)
                    list_below.append(p2)
                
                elif p1_test=='uder' and p2_test=='under':
                    list_below.append(p2)
            i+=1
            
        xover = [p[0] for p in list_above]
        yover = [p[1] for p in list_above]
        
        xunder = [p[0] for p in list_below]
        yunder = [p[1] for p in list_below]
        
        #plt.plot(xover,yover,'co')
        #plt.plot(xunder, yunder,'ko')
        
        if solid==False:
            list_above.reverse()
    
        int_count = 0
        xsub = []
        ysub = []
        xsub2 = []
        ysub2 = []
        
        if len(list_above) >=3:
            if list_above[0][1] == list_above[1][1] and list_above[0][1]==line_y:
                
                xsub = [p[0] for p in list_above]
                ysub = [p[1] for p in list_above]
                sub = Section(xsub,ysub,solid,n)
                sub_shapes.append(sub)
            
            elif list_above[0][1] != line_y and len([1 for p in list_above if p[1]==line_y])>=2:
                xsub = [p[0] for p in list_above]
                ysub = [p[1] for p in list_above]
                sub = Section(xsub,ysub,solid,n)
                sub_shapes.append(sub)
                
            else:
                xsub = []
                ysub = []
                xsub2 = []
                ysub2 = []
                i=0
                for point in list_above:
                    if list_above[0][1]!=line_y and int_count<1:
                        xsub2.append(point[0])
                        ysub2.append(point[1])
                    
                    else:
                        if int_count > 2:
                            xsub2.append(point[0])
                            ysub2.append(point[1])
                        else:
                            xsub.append(point[0])
                            ysub.append(point[1])
    
                    
                    if point != list_above[-1]:
                        next_point = list_above[i+1]
                        prev_point = list_above[i-1]
                        next_point_check = next_point[1] == line_y and point[1] == line_y and next_point[0]> point[0]
                        prev_point_check = prev_point[1] == line_y and point[1] >= prev_point[1] and next_point[1] > point[1]
                        if prev_point_check == True:
                            int_count = 0
                    else:
                        next_point_check = False
                        prev_point_check = False
                    
                    if point[1] == line_y:
                        int_count +=1
                    
                    if int_count >= 2 and len(xsub)>2 and list_above[0][1]==line_y and next_point_check==False:
                        sub = Section(xsub,ysub,solid,n)
                        int_count = 0
                        xsub = []
                        ysub = []
                        
                        sub_shapes.append(sub)
                    
                    elif point == list_above[-1] and len(xsub)>2:
                        sub = Section(xsub,ysub,solid,n)
                        int_count = 0
                        xsub = []
                        ysub = []
                        
                        sub_shapes.append(sub)
                    
                    i+=1
    
        if len(xsub2)>2:
            sub = Section(xsub2,ysub2,solid,n)
            int_count = 0
            xsub = []
            ysub = []
            
            sub_shapes.append(sub)
        
                    
    return sub_shapes       

def stl_wf(d,bf,tf,tw,k):
    '''
    given the defining geometric
    properties for a Wide Flange from
    AISC 
    
    return a Shape with appropriate
    coordinates
    0,0 point will be the bottom left of the section
    '''
    
    # Bottom flange
    x = [0,bf,bf]
    y = [0,0,tf]
    
    # points in bottom right radius angle range is 270,180
    cr1x = (bf/2.0)+(tw/2.0)+(k-tf)
    cr1y = k
    
    # draw circle for radius in clockwise order then reverse it
    # for the first radius
    r=k-tf
    x_r1, y_r1 = circle_coordinates(cr1x,cr1y,r,180,270)
    
    x_r1.reverse()
    y_r1.reverse()
    
    x.extend(x_r1)
    y.extend(y_r1)

    # points in top right radius angle range is 180,90
    cr2x = cr1x
    cr2y = d-k
    
    # draw circle for radius in clockwise order then reverse it
    # for the first radius
    x_r2, y_r2 = circle_coordinates(cr2x,cr2y,r,90,180)
    
    x_r2.reverse()
    y_r2.reverse()
    
    x.extend(x_r2)
    y.extend(y_r2)
    
    # top flange
    x.extend([bf,bf,0,0])   
    y.extend([d-tf,d,d,d-tf])

    # points in top left radius angle range is 90,0
    cr3x = (bf/2.0)-(tw/2.0)-(k-tf)
    cr3y = d-k
    
    # draw circle for radius in clockwise order then reverse it
    # for the first radius
    x_r3, y_r3 = circle_coordinates(cr3x,cr3y,r,0,90)
    
    x_r3.reverse()
    y_r3.reverse()
    
    x.extend(x_r3)
    y.extend(y_r3)

    # points in bottom left radius angle range is 360,270
    cr4x = cr3x
    cr4y = k
    
    # draw circle for radius in clockwise order then reverse it
    # for the first radius
    x_r4, y_r4 = circle_coordinates(cr4x,cr4y,r,270,360)
    
    x_r4.reverse()
    y_r4.reverse()
    
    x.extend(x_r4)
    y.extend(y_r4)
    
    # Last points to close the bottom flange
    x.extend([0,0])
    y.extend([tf,0])
    
    WF = Section(x,y)
    
    return WF
    
def stl_angle(vleg, hleg, thickness, k):
    '''
    given the defining geometric
    properties for an Angle from
    AISC 
    
    return a Shape with appropriate
    coordinates
    0,0 point will be the bottom left of the section
    '''
    r1 = k - thickness # leg-to-leg Fillet
    r2 = r1/2.0        # toe fillet 1/2*Fillet per ISO 657-1: 1989 (E)
    
    # Bottom horizontal leg
    x = [0,hleg,hleg]
    y = [0,0,thickness - r2]
    
    # outisde horizontal leg fillet
    # for the first radius
    r=r2
    x_r1, y_r1 = circle_coordinates(hleg-(r2),thickness - r2,r,1,90)
    
    x.extend(x_r1)
    y.extend(y_r1)
    
    # horizontal top flat   
    x.append(k)
    y.append(thickness)
    
    #interior corner radii    
    r = r1
    x_r1, y_r1 = circle_coordinates(k,k,r,180,269)
    
    x_r1.reverse()
    y_r1.reverse()
    
    x.extend(x_r1)
    y.extend(y_r1)
    
    # vertical inside flat
    x.append(thickness)
    y.append(vleg - r2)
    
    # outside vertical leg fillet
    r=r2
    x_r1, y_r1 = circle_coordinates(thickness - r2,vleg-(r2),r,1,90)
    
    x.extend(x_r1)
    y.extend(y_r1)
    
    x.append(0)
    y.append(vleg)
    
    x.append(0)
    y.append(0)
    
    Angle = Section(x,y)
    
    return Angle






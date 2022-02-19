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


def center_of_two_points(p1=[0, 0], p2=[1, 1]):
    x_center = (p1[0]+p2[0])/2.0
    y_center = (p1[1]+p2[1])/2.0

    return (x_center, y_center)


def length_between_two_points(p1=[0, 0], p2=[1, 1]):
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])

    length = (dx**2 + dy**2)**0.5

    return length


def parrallel_axis_theorem(momentofinertia=1, area=1,
                           distancetoparallelaxis=1):
    '''
    Parralel axis theorem: I' = Ilocal + A*d^2
    '''
    return (momentofinertia
            + (area*distancetoparallelaxis*distancetoparallelaxis))


def centroid_by_areas(areas=[0], areacenters=[[0, 0]], referencepoint=[0, 0]):
    '''
    computes the centroid x,y distances from a reference point
    and returns the global x,y coordinates relative to (0,0)

    length of areas and areacenters must be equal
    '''
    if len(areas) != len(areacenters):
        return 'Number of Areas needs to match the number of Area Centers'
    else:
        sumA = sum(areas)
        sumAx = 0
        sumAy = 0
        for area, areacenter in zip(areas, areacenters):
            cix = areacenter[0] - referencepoint[0]
            ciy = areacenter[1] - referencepoint[1]

            sumAx = sumAx + (area*cix)
            sumAy = sumAy + (area*ciy)

        Cx = sumAx/sumA
        Cy = sumAy/sumA

        global_center_x = Cx + referencepoint[0]
        global_center_y = Cy + referencepoint[1]

        return (global_center_x, global_center_y)


class weld_segment:
    def __init__(self, startcoordinates=[0, 0], endcoordinates=[1, 1], suid=1):

        self.start = startcoordinates

        self.end = endcoordinates

        self.suid = suid

        self.m = self.end[0] - self.start[0]
        self.n = self.end[1] - self.start[1]

        self.center = center_of_two_points(self.start, self.end)

        self.length = length_between_two_points(self.start, self.end)
        self.area = self.length

        self.Ixo = (self.length*self.n*self.n)/12.0

        self.Iyo = (self.length*self.m*self.m)/12.0

        self.x_coords = [self.start[0], self.end[0]]
        self.y_coords = [self.start[1], self.end[1]]

        self.sigma_x_i = None
        self.sigma_y_i = None
        self.sigma_z_i = None
        self.sigma_x_j = None
        self.sigma_y_j = None
        self.sigma_z_j = None
        self.sigma_x_m = None
        self.sigma_y_m = None
        self.sigma_z_m = None
        self.sigma_i = None
        self.sigma_j = None
        self.sigma_m = None

        self.Ixx = None
        self.Iyy = None
        self.dxi = None
        self.dyi = None
        self.dxj = None
        self.dyj = None
        self.dxm = None
        self.dym = None

    def global_moments_of_inertia(self, referencepoint=[0, 0]):

        Cx = self.center[0] - referencepoint[0]
        Cy = self.center[1] - referencepoint[1]

        self.Ixx = parrallel_axis_theorem(self.Ixo, self.area, Cy)
        self.Iyy = parrallel_axis_theorem(self.Iyo, self.area, Cx)
        self.Ixy = self.length*Cx*Cy

        return (self.Ixx, self.Iyy, self.Ixy)

    def distance_from_segment_nodes_to_reference(self, referencepoint=[0, 0]):

        x = referencepoint[0]
        y = referencepoint[1]

        xi = self.start[0]
        yi = self.start[1]
        xj = self.end[0]
        yj = self.end[1]
        xm = self.center[0]
        ym = self.center[1]

        self.dxi = xi - x
        self.dyi = yi - y
        self.dxj = xj - x
        self.dyj = yj - y
        self.dxm = xm - x
        self.dym = ym - y

    def set_segment_stresses(self,
                             sigma_xi, sigma_yi, sigma_zi,
                             sigma_xj, sigma_yj, sigma_zj,
                             sigma_xm, sigma_ym, sigma_zm):

        self.sigma_xi = sigma_xi
        self.sigma_yi = sigma_yi
        self.sigma_zi = sigma_zi
        self.sigma_xj = sigma_xj
        self.sigma_yj = sigma_yj
        self.sigma_zj = sigma_zj
        self.sigma_xm = sigma_xm
        self.sigma_ym = sigma_ym
        self.sigma_zm = sigma_zm

        # compute end stress magnitute from
        # square root of the sum of squares
        self.sigma_i = math.sqrt((sigma_xi*sigma_xi)
                                    + (sigma_yi*sigma_yi)
                                    + (sigma_zi*sigma_zi))
        self.sigma_j = math.sqrt((sigma_xj*sigma_xj)
                                    + (sigma_yj*sigma_yj)
                                    + (sigma_zj*sigma_zj))
        self.sigma_m = math.sqrt((sigma_xm*sigma_xm)
                                    + (sigma_ym*sigma_ym)
                                    + (sigma_zm*sigma_zm))


class elastic_weld_group:
    def __init__(self, weld_segments=[weld_segment([0, 0], [0, 1])]):

        self.weld_segments = weld_segments

        # build lists of areas and center of areas for each weld segment to
        # pass into the centroid_by_areas function

        areas = [weld.area for weld in weld_segments]
        areacenters = [weld.center for weld in weld_segments]

        # Weld Group area = sum of the weld segment lengths
        self.Area = sum(areas)

        # Determine the centroid coordinates for the weld group
        self.group_center = centroid_by_areas(areas, areacenters)
        self.Cx = self.group_center[0]
        self.Cy = self.group_center[1]
        self.centroid_web = f'{{x: {self.Cx:.3f}, y: {self.Cy:.3f}}}'

        # Determine Ix and Iy about the weld group centroidal axis
        self.Ixx = 0
        self.Iyy = 0
        self.Ixy = 0

        for weld in weld_segments:

            Isegmentgroup = weld.global_moments_of_inertia(self.group_center)

            self.Ixx = self.Ixx + Isegmentgroup[0]
            self.Iyy = self.Iyy + Isegmentgroup[1]
            self.Ixy = self.Ixy + Isegmentgroup[2]

        # Polar Moment of Inertia for Torsion stresses
        self.Ip = self.Ixx + self.Iyy

        # Denominator in General form of the stress equation
        # precompute this for cleaner entry later
        # unit are length ^ 8
        self.IxxIyy_Ixy2 = (self.Ixx*self.Iyy)-(self.Ixy*self.Ixy)

        # setup error and warning lists
        self.warnings = []
        self.errors = []

    def force_analysis(self, Fz, Fx, Fy, Mx, My, T):

        # Assumes forces are applied at the weld group centroid
        # Utilizes the general bending stress formula to capture
        # bending about non-principal axis.

        # Direct Stresses
        sigma_z_direct = Fz/self.Area
        sigma_x_direct = Fx/self.Area
        sigma_y_direct = Fy/self.Area

        max_sigma = 0

        num_segments = len(self.weld_segments)

        # Additional Stresses by Segment
        for weld in self.weld_segments:

            # get the dx, dy distances for the segment ends and mid point

            weld.distance_from_segment_nodes_to_reference(self.group_center)

            dxi = weld.dxi
            dyi = weld.dyi
            dxj = weld.dxj
            dyj = weld.dyj
            dxm = weld.dxm
            dym = weld.dym

            # segment start
            # sigma z from bending
            if (self.Iyy == 0 and self.Ixx !=0):
                sigma_zyi_Mx = (Mx*dyi)/self.Ixx
                sigma_zyi_My = 0
                sigma_zxi_Mx = 0
                sigma_zxi_My = 0
                sigma_zi_M = (sigma_zyi_Mx
                                + sigma_zyi_My
                                + sigma_zxi_Mx
                                + sigma_zxi_My)

                self.warnings.append('Iyy of weld group is 0 -- My cannot be resisted')
            elif (self.Ixx == 0 and self.Iyy != 0):
                sigma_zyi_Mx = 0
                sigma_zyi_My = 0
                sigma_zxi_Mx = 0
                sigma_zxi_My = (-1*My*dxi)/self.Iyy
                sigma_zi_M = (sigma_zyi_Mx
                                + sigma_zyi_My
                                + sigma_zxi_Mx
                                + sigma_zxi_My)

                self.warnings.append('Ixx of weld group is 0 -- Mx cannot be resisted')

            elif (self.Ixx == 0 or self.Iyy == 0):
                sigma_zyi_Mx = 0
                sigma_zyi_My = 0
                sigma_zxi_Mx = 0
                sigma_zxi_My = 0
                sigma_zi_M = (sigma_zyi_Mx
                                + sigma_zyi_My
                                + sigma_zxi_Mx
                                + sigma_zxi_My)

                self.warnings.append('Ixx and Iyy of weld group are 0 -- bending cannot be resisted')
            else:
                sigma_zyi_Mx = (Mx*dyi*self.Iyy)/self.IxxIyy_Ixy2
                sigma_zyi_My = (My*dyi*self.Ixy)/self.IxxIyy_Ixy2
                sigma_zxi_Mx = (-1*Mx*dxi*self.Ixy)/self.IxxIyy_Ixy2
                sigma_zxi_My = (-1*My*dxi*self.Ixx)/self.IxxIyy_Ixy2
                sigma_zi_M = (sigma_zyi_Mx
                                + sigma_zyi_My
                                + sigma_zxi_Mx
                                + sigma_zxi_My)

            # Total sigma z
            sigma_zi = sigma_zi_M + sigma_z_direct

            # sigma x from torsion
            sigma_xi_T = (-1*T*dyi)/self.Ip

            # Total sigma x
            sigma_xi = sigma_xi_T + sigma_x_direct

            # sigma y from torsion
            sigma_yi_T = (T*dxi)/self.Ip

            # Total sigma y
            sigma_yi = sigma_yi_T + sigma_y_direct

            # square root of sum of squares
            sigma_i = math.sqrt(
                                (sigma_xi*sigma_xi)
                                + (sigma_yi*sigma_yi)
                                + (sigma_zi*sigma_zi))

            # segment end
            # sigma z from bending
            if (self.Iyy == 0 or self.Ixx == 0):
                sigma_zyj_Mx = 0
                sigma_zyj_My = 0
                sigma_zxj_Mx = 0
                sigma_zxj_My = 0
                sigma_zj_M = 0
            else:
                sigma_zyj_Mx = (Mx*dyj*self.Iyy)/self.IxxIyy_Ixy2
                sigma_zyj_My = (My*dyj*self.Ixy)/self.IxxIyy_Ixy2
                sigma_zxj_Mx = (-1*Mx*dxj*self.Ixy)/self.IxxIyy_Ixy2
                sigma_zxj_My = (-1*My*dxj*self.Ixx)/self.IxxIyy_Ixy2
                sigma_zj_M = (sigma_zyj_Mx
                                + sigma_zyj_My
                                + sigma_zxj_Mx
                                + sigma_zxj_My)

            # Total sigma z
            sigma_zj = sigma_zj_M + sigma_z_direct

            # sigma x from torsion
            sigma_xj_T = (-1*T*dyj)/self.Ip

            # Total sigma x
            sigma_xj = sigma_xj_T + sigma_x_direct

            # sigma y from torsion
            sigma_yj_T = (T*dxj)/self.Ip

            # Total sigma y
            sigma_yj = sigma_yj_T + sigma_y_direct

            # square root of sum of squares
            sigma_j = math.sqrt(
                                (sigma_xj*sigma_xj)
                                + (sigma_yj*sigma_yj)
                                + (sigma_zj*sigma_zj))

            # segment midpoint
            # sigma z from bending
            if (self.Iyy == 0 or self.Ixx == 0):
                sigma_zym_Mx = 0
                sigma_zym_My = 0
                sigma_zxm_Mx = 0
                sigma_zxm_My = 0
                sigma_zm_M = 0

            else:
                sigma_zym_Mx = (Mx*dym*self.Iyy)/self.IxxIyy_Ixy2
                sigma_zym_My = (My*dym*self.Ixy)/self.IxxIyy_Ixy2
                sigma_zxm_Mx = (-1*Mx*dxm*self.Ixy)/self.IxxIyy_Ixy2
                sigma_zxm_My = (-1*My*dxm*self.Ixx)/self.IxxIyy_Ixy2
                sigma_zm_M = (sigma_zym_Mx
                                + sigma_zym_My
                                + sigma_zxm_Mx
                                + sigma_zxm_My)

            # Total sigma z
            sigma_zm = sigma_zm_M + sigma_z_direct

            # sigma x from torsion
            sigma_xm_T = (-1*T*dym)/self.Ip

            # Total sigma x
            sigma_xm = sigma_xm_T + sigma_x_direct

            # sigma y from torsion
            sigma_ym_T = (T*dxm)/self.Ip

            # Total sigma y
            sigma_ym = sigma_ym_T + sigma_y_direct

            # square root of sum of squares
            sigma_m = math.sqrt(
                                (sigma_xm*sigma_xm)
                                + (sigma_ym*sigma_ym)
                                + (sigma_zm*sigma_zm))

            weld.set_segment_stresses(sigma_xi, sigma_yi, sigma_zi,
                                        sigma_xj, sigma_yj, sigma_zj,
                                        sigma_xm, sigma_ym, sigma_zm)

            max_sigma = max(max_sigma, sigma_i, sigma_j, sigma_m)

        return max_sigma

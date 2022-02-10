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

class reinforcement:
    def __init__(self,fy_ksi):
        self.bar = {0:[0.0,0.0], 3:[0.375,0.11], 4: [0.5,0.2], 5: [0.625,0.31], 6: [0.75,0.44], 7: [0.875,0.6], 8: [1,0.79], 9: [1.128,1], 10: [1.27,1.27], 11: [1.41,1.56], 14: [1.693,2.25], 18: [2.257,4]}
        self.fy_ksi = float(fy_ksi)
        self.fy_psi = self.fy_ksi * 1000.0
        self.Es_ksi = 29000.0
        self.Es_psi = self.Es_ksi * 1000.0

class t_beam:
    def __init__(self, b_in, h_in, h_slab_in, beam_span_ft, slab_span_left_ft, slab_span_right_ft, bf_in, hf_in, f_prime_c_psi,density_pcf):

        self.bw_in = float(b_in)
        self.h_in = float(h_in)
        self.f_prime_c_psi = float(f_prime_c_psi)

        #calculation of effective flange width per ACI 318-08 section 8.12

        #Section 8.12.3 - for slab on one side only
        if float(slab_span_left_ft) == 0 and float(slab_span_right_ft) != 0:
            self.bf_left_in = 0
            self.bf_right_in = min((1/12.0)*float(beam_span_ft)*12,6*float(h_slab_in),(1/2.0)*float(slab_span_right_ft)*12)
            self.bf_in = self.bw_in + self.bf_right_in
            self.bf_status = 'OK'
            self.hf_in = float(h_slab_in)
        elif float(slab_span_right_ft) == 0 and float(slab_span_left_ft) != 0:
            self.bf_left_in = min((1/12.0)*float(beam_span_ft)*12,6*float(h_slab_in),(1/2.0)*float(slab_span_left_ft)*12)
            self.bf_right_in = 0
            self.bf_in = self.bw_in + self.bf_left_in
            self.bf_status = 'OK'
            self.hf_in = float(h_slab_in)
        #Section 8.12.4 - Assumes user wants to use their own flange, expects bf_in and hf_in to be non-zero
        elif float(slab_span_left_ft) == 0 and float(slab_span_right_ft) == 0 and float(beam_span_ft) ==0:
            if float(bf_in) <= 0 and float(hf_in) <=0:
                self.bf_status = 'OK, rectangular section with no flange'
                self.bf_in = self.bw_in
                self.hf_in = 0
                self.bf_left_in = 0
                self.bf_right_in = self.bf_left_in

            else:
                if float(hf_in) < (1/2.0)*self.bw_in:
                    self.bf_status = 'NG see ACI 318-08 section 8.12.4, Hf revised to 0.5*Bw'
                    self.hf_in = (1/2.0)*self.bw_in
                    if float(bf_in) > 4*self.bw_in:
                        self.bf_status = self.bf_status + '\nNG see ACI 318-08 section 8.12.4, Bf revised to 4*Bw'
                        self.bf_in = 4*self.bw_in
                        self.bf_left_in = (self.bf_in - self.bw_in)/2
                        self.bf_right_in = self.bf_left_in
                    else:
                        self.bf_in = float(bf_in)
                        self.bf_left_in = (self.bf_in - self.bw_in)/2
                        self.bf_right_in = self.bf_left_in
                        self.bf_status = self.bf_status + '\nBf OK'
                else:
                    if float(bf_in) > 4*self.bw_in:
                        self.bf_status = 'NG see ACI 318-08 section 8.12.4, Bf revised to 4*Bw'
                        self.bf_in = 4*self.bw_in
                        self.hf_in = float(hf_in)
                        self.bf_left_in = (self.bf_in - self.bw_in)/2
                        self.bf_right_in = self.bf_left_in
                    else:
                        self.bf_in = float(bf_in)
                        self.hf_in = float(hf_in)
                        self.bf_left_in = (self.bf_in - self.bw_in)/2
                        self.bf_right_in = self.bf_left_in
                        self.bf_status = 'OK'
        #Section 8.12.2 - Slab on both sides
        else:
            self.bf_max_in = (1/4.0)*float(beam_span_ft)*12
            self.bf_max_left_in = (self.bf_max_in - self.bw_in)/2
            self.bf_max_right_in = self.bf_max_left_in

            self.bf_left_in = min(8*float(h_slab_in),(1/2.0)*float(slab_span_left_ft)*12,self.bf_max_left_in)
            self.bf_right_in = min(8*float(h_slab_in),(1/2.0)*float(slab_span_right_ft)*12,self.bf_max_right_in)

            self.bf_in = self.bf_left_in + self.bw_in + self.bf_right_in
            self.hf_in = float(h_slab_in)
            self.bf_status = 'OK'
        
        self.hw_in = self.h_in - self.hf_in
        
        self.bfbwmax = max(self.bf_in,self.bw_in)
        self.hbfbwmax = max(self.h_in,self.bfbwmax)

        #Calculate Igross neglecting steel
        self.Af_in2 = self.bf_in * self.hf_in
        self.If_in4 = (self.bf_in * self.hf_in**3)/12
        self.Aw_in2 = self.bw_in * self.hw_in
        self.Iw_in4 = (self.bw_in * self.hw_in**3)/12
        self.cgy_in = (self.Af_in2*((self.hf_in/2.0)+self.hw_in) + self.Aw_in2*(self.hw_in/2.0))/(self.Af_in2+self.Aw_in2)
        self.df_in = abs(((self.hf_in/2.0)+self.hw_in)-self.cgy_in)
        self.dw_in = abs((self.hw_in/2.0)-self.cgy_in)
        self.Ig_in4 = self.If_in4 + (self.Af_in2*self.df_in**2) + self.Iw_in4 + (self.Aw_in2*self.dw_in**2)

        #section vertex coordinates to make plotting easier
        self.section_x_coords_in = [0,self.bw_in,self.bw_in,self.bf_right_in+self.bw_in,self.bf_right_in+self.bw_in,-1*self.bf_left_in,-1*self.bf_left_in,0,0]
        self.section_y_coords_in = [0,0,self.hw_in,self.hw_in,self.h_in,self.h_in,self.hw_in,self.hw_in,0]


        if 90 <= density_pcf <= 160:
            self.Ec_psi = density_pcf**1.5 * 33 * self.f_prime_c_psi**(1/2.0)
        else:
            self.Ec_psi = 'Density of Concrete must be between 90 and 160 PCF'

        self.weight_plf = (self.Af_in2+self.Aw_in2) * (1/144) * density_pcf
        self.Ag_in2 = (self.Af_in2+self.Aw_in2)
        self.weight_klf = self.weight_plf/1000.0
        self.fr_psi = 7.5 * self.f_prime_c_psi**(1/2.0)
        self.Mcrack_inlbs = (self.fr_psi*self.Ig_in4)/(self.cgy_in)
        self.Mcrack_ftlbs = self.Mcrack_inlbs/12.0
        self.Mcrack_ftkips = self.Mcrack_ftlbs/1000.0

        if self.f_prime_c_psi <= 4000:
            self.beta1 = 0.85
        elif self.f_prime_c_psi <= 8000:
            self.beta1 = 0.85 - ((0.05*(self.f_prime_c_psi-4000))/1000)
        else:
            self.beta1 = 0.65

    def as_min(self,d_in,fy_psi):
        return max((3 * self.f_prime_c_psi**(1/2.0) * self.bw_in * d_in)/fy_psi, (200.0 * self.bw_in * d_in)/fy_psi)

    def max_bars_layer(self,flexural_bar, cover_in, shear_bar, aggregate_size_in):

        self.first_interior_bar_in = cover_in + shear_bar[0] + 2*shear_bar[0]

        min_spacing = max(1,flexural_bar[0],1.33*aggregate_size_in)+flexural_bar[0]

        num_interior_bars = 1 + ((self.bw_in - 2*self.first_interior_bar_in)/min_spacing)

        return math.floor(num_interior_bars)

    def min_bars_bottom_layer(self,reinf_bar,cover_in, shear_bar, fy_psi):
        fs = (2/3.0)*fy_psi
        cc = cover_in + shear_bar[0]

        first_interior_bar_in = cover_in + shear_bar[0] + 2*shear_bar[0]

        min_spacing = (15*(40000/fs)) - 2.5*cc

        num_interior_bars = 1 + ((self.bw_in - 2*first_interior_bar_in)/min_spacing)

        return math.ceil(num_interior_bars)

    def flexural_bottom_bars_automatic_by_layers(self,flexural_bars_array,flexural_bar_count_array,cover_in,shear_bar):
        bottom_bars_as = []
        bottom_bars_d = []
        bottom_bars_cg = 0

        i=0
        for bars in flexural_bar_count_array:
            bottom_bars_as.append(bars*flexural_bars_array[i][1])
            if i==0:
                bottom_bars_d.append(self.h_in - (cover_in + shear_bar[0] + (flexural_bars_array[i][0] * 0.5)))
            else:
                bottom_bars_d.append(bottom_bars_d[i-1] - (1 + flexural_bars_array[i-1][0] * 0.5 + flexural_bars_array[i][0] * 0.5))
            i+=1

        total_as = sum(bottom_bars_as)
        total_as_d = 0
        i=0
        for i in range(len(bottom_bars_as)):
            total_as_d = total_as_d + (bottom_bars_as[i]*bottom_bars_d[i])

        bottom_bars_cg = total_as_d/total_as
        return bottom_bars_as, bottom_bars_d, bottom_bars_cg

    def flexural_top_bars_automatic_by_layers(self,flexural_bars_array,flexural_bar_count_array,cover_in,shear_bar):
        top_bars_as = []
        top_bars_d = []

        i=0
        for bars in flexural_bar_count_array:
            top_bars_as.append(bars*flexural_bars_array[i][1])
            if i==0:
                top_bars_d.append((cover_in + shear_bar[0] + (flexural_bars_array[i][0] * 0.5)))
            else:
                top_bars_d.append(top_bars_d[i-1] + (1 + flexural_bars_array[i-1][0] * 0.5 + flexural_bars_array[i][0] * 0.5))
            i+=1

        total_as = sum(top_bars_as)
        total_as_d = 0
        i=0
        for i in range(len(top_bars_as)):
            total_as_d = total_as_d + (top_bars_as[i]*top_bars_d[i])
        
        top_bars_cg = total_as_d/total_as
        
        return top_bars_as, top_bars_d, top_bars_cg

    def strain_compatibility_steel(self,bars_as_array,bars_d_array,c_in,fy_psi,Es_psi):
        steel_strain = []
        steel_stress = []
        steel_tension_force_layer_lbs = []
        steel_tension_force_lbs = 0
        i=0
        for i in range(len(bars_as_array)):
            steel_strain.append(0.003*((bars_d_array[i]/c_in)-1))
            fs = steel_strain[i] * Es_psi
            if fs < -1*fy_psi or fs > fy_psi:
                if fs<0:
                    steel_stress.append((fs/abs(fs))*fy_psi)
                    
                    if bars_d_array[i] < self.beta1*c_in:
                        steel_tension_force_layer_lbs.append((((fs/abs(fs))*fy_psi)+0.85*self.f_prime_c_psi)*bars_as_array[i])
                    else:
                        steel_tension_force_layer_lbs.append((((fs/abs(fs))*fy_psi))*bars_as_array[i])
                else:
                    steel_stress.append((fs/abs(fs))*fy_psi)
                    steel_tension_force_layer_lbs.append(((fs/abs(fs))*fy_psi)*bars_as_array[i])
            else:
                if fs<0:
                    steel_stress.append(fs)
                    
                    if bars_d_array[i] < self.beta1*c_in:
                        steel_tension_force_layer_lbs.append((fs+0.85*self.f_prime_c_psi)*bars_as_array[i])
                    else:
                        steel_tension_force_layer_lbs.append((fs)*bars_as_array[i])
                else:
                    steel_stress.append(fs)
                    steel_tension_force_layer_lbs.append(fs*bars_as_array[i])

        steel_tension_force_lbs = sum(steel_tension_force_layer_lbs)

        return steel_strain,steel_stress,steel_tension_force_layer_lbs,steel_tension_force_lbs

    def strain_compatibility_concrete(self,c_in):
        a = self.beta1 * c_in
        if a <= self.hf_in or self.hf_in == 0:
            compression_block_in2 = self.bf_in * a
            compression_block_cg_top = a/2
        else:
            compression_block_in2 = (self.bf_in * self.hf_in) + (self.bw_in*(a-self.hf_in))
            compression_block_cg_top = (self.Af_in2*(self.hf_in/2.0) + (self.bw_in*(a-self.hf_in))*(((a-self.hf_in)/2.0)+self.hf_in))/compression_block_in2
        concrete_compression_force_lbs = 0.85 * self.f_prime_c_psi * compression_block_in2

        return concrete_compression_force_lbs, compression_block_cg_top

    def find_pna(self,bars_as_array,bars_d_array,bars_cg,fy_psi,Es_psi):
        a=0
        b=max(bars_d_array)
        c=0
        pna = 0

        loop_max = 10000
        tol = 0.0000000000001
        loop = 0

        while loop<loop_max:
            c = (a+b)/2
            strain_c, stress_c, layer_c, tension_c = self.strain_compatibility_steel(bars_as_array,bars_d_array,c,fy_psi,Es_psi)
            compression_c, compression_cg_top = self.strain_compatibility_concrete(c)
            
            if compression_c == tension_c or (b-a)/2 <= tol:
                pna = c
                loop = loop_max
            elif compression_c > tension_c:
                b = c
            else:
                a = c
            loop+=1
            #print(tension_c)
            #print(pna)
        return pna

    def moment_capacity_inlbs(self,bars_as_array,bars_d_array,bars_cg,c_in,fy_psi,Es_psi):
        self.x_strain = []
        self.y_strain = []
        a = self.beta1 * c_in
        if a <= self.hf_in or self.hf_in == 0:
            compression_block_in2 = self.bf_in * a
            compression_block_cg_top = a/2
        else:
            compression_block_in2 = (self.bf_in * self.hf_in) + (self.bw_in*(a-self.hf_in))
            compression_block_cg_top = (self.Af_in2*(self.hf_in/2.0) + (self.bw_in*(a-self.hf_in))*(((a-self.hf_in)/2.0)+self.hf_in))/compression_block_in2
        concrete_compression_force_lbs = 0.85 * self.f_prime_c_psi * compression_block_in2
        self.x_strain.append(0)
        self.y_strain.append(self.h_in)
        self.x_strain.append(-.003)
        self.y_strain.append(self.h_in)
        steel_strain = []
        steel_stress = []
        steel_tension_force_layer_lbs = []
        steel_moment_component_inlbs = 0
        i=0
        for i in range(len(bars_as_array)):
            steel_strain.append(0.003*((bars_d_array[i]/c_in)-1))
            self.x_strain.append(steel_strain[i])
            self.y_strain.append(self.h_in - bars_d_array[i])
            fs = steel_strain[i] * Es_psi
            if fs < -1*fy_psi or fs > fy_psi:
                steel_stress.append((fs/abs(fs))*fy_psi)
                
                if fs<0:
                    steel_tension_force_layer_lbs.append(((((fs/abs(fs))*fy_psi))+0.85*self.f_prime_c_psi)*bars_as_array[i])
                else:
                    steel_tension_force_layer_lbs.append(((fs/abs(fs))*fy_psi)*bars_as_array[i])
                steel_moment_component_inlbs = steel_moment_component_inlbs + (steel_tension_force_layer_lbs[i]*(bars_d_array[i]-bars_cg))
            else:
                steel_stress.append(fs)
                if fs<0:
                    steel_tension_force_layer_lbs.append((fs+0.85*self.f_prime_c_psi)*bars_as_array[i])
                else:
                    steel_tension_force_layer_lbs.append(fs*bars_as_array[i])
                steel_moment_component_inlbs = steel_moment_component_inlbs + (steel_tension_force_layer_lbs[i]*(bars_d_array[i]-bars_cg))
        self.x_strain.append(0)
        self.y_strain.append(self.h_in - max(bars_d_array))
        if max(steel_strain)<0.004:
            return 0,0,0
        else:
            if max(steel_strain)>=0.005:
                phi = 0.9
            else:
                phi = 0.65 + ((max(steel_strain)-0.002)*(250/3))

            concrete_moment_arm_in = bars_cg - compression_block_cg_top
            concrete_moment_component_inlbs = concrete_compression_force_lbs * concrete_moment_arm_in
            nominal_moment_inlbs = concrete_moment_component_inlbs + steel_moment_component_inlbs

            return phi,nominal_moment_inlbs,phi*nominal_moment_inlbs

    def concrete_shear_capacity_lbs(self,bars_cg, shear_bars_fy_psi, shear_bar_area_in2):
        phi = 0.75
        
        #ACI 318-08 11.1.2 sqrt(f'c) limited to 100 psi
        if self.f_prime_c_psi > 10000:
            vc_fprimec_psi = 10000
        else:
            vc_fprimec_psi = self.f_prime_c_psi

        #ACI 318-08 11.2.1 equation 11-3
        vc = 2*self.bw_in*bars_cg*vc_fprimec_psi**(1/2.0)
        phivc = phi*vc
        
        #ACI 318-08 11.4.2 limits shear bars to 60 ksi
        if shear_bars_fy_psi > 60000:
            fyt_psi = 60000
        else:
            fyt_psi = shear_bars_fy_psi
            
        #ACI 318-08 11.4.5.1 - assumes vertical stirrups
        self.max_shear_spacing_in = min(bars_cg/2.0,24)
        
        #ACI 318-08 11.4.6.3 - Av,min/s
        self.av_min_s = min(0.75*vc_fprimec_psi**(1/2.0)*self.bw_in*(1.0/fyt_psi),50*self.bw_in*(1.0/fyt_psi))
        
        #ACI 318-08 11.4.7.2 equation 11-15 - assumes vertical stirrups
        self.s_Vs_2_legs = 2*shear_bar_area_in2*fyt_psi*bars_cg
        self.s_Vs_4_legs = 4*shear_bar_area_in2*fyt_psi*bars_cg
        self.s_Vs_6_legs = 6*shear_bar_area_in2*fyt_psi*bars_cg
        
        #ACI 318-08 11.4.7.9
        vsmax = 8*self.bw_in*bars_cg*vc_fprimec_psi**(1/2.0)
        phivsmax = phi*vsmax
        vnmax = vc + vsmax
        phivnmax = phi*vnmax

        return phi, vc, phivc, vsmax, vnmax, phivnmax
        
    def concrete_threshold_torsion_inlbs(self):
        phi = 0.75
        
        #ACI 318-08 11.1.2 sqrt(f'c) limited to 100 psi
        if self.f_prime_c_psi > 10000:
            vc_fprimec_psi = 10000
        else:
            vc_fprimec_psi = self.f_prime_c_psi
        
        #Calculation of Acp and Pcp
        rect_Acp_in2 = self.bw_in*self.h_in
        rect_Pcp_in = (2.0*self.bw_in)+(2.0*self.h_in)
        area_over_perim_rect = (rect_Acp_in2**2.0) / rect_Pcp_in
        
        #ACI 318-08 11.5.1.1 - T beam consraints per 13.2.4
        if self.bf_left_in == 0 or self.bf_right_in == 0:
            if self.bf_left_in == 0 and self.bf_right_in == 0:
                self.Acp_in2 = rect_Acp_in2
                self.Pcp_in = rect_Pcp_in
                self.Torsion_threshold = vc_fprimec_psi**(1/2.0) * area_over_perim_rect
                self.AoP_status = 'Rectangular Section used for Acp and Pcp'
            elif self.bf_left_in ==0:
                Torsion_bf_right_in = min(self.bf_right_in, self.hw_in, 4*self.hf_in)
                Acp_in2 = (self.bw_in*self.hw_in) + ((self.bw_in+Torsion_bf_right_in)*self.hf_in)
                Pcp_in = self.bw_in + self.hw_in + Torsion_bf_right_in + self.hf_in + Torsion_bf_right_in + self.bw_in + self.h_in
                
                #Check Acp^2/Pcp of T Beam not less than for Rectangular beam
                area_over_perim_t = (Acp_in2**2.0)/Pcp_in
                
                if area_over_perim_rect > area_over_perim_t:
                    self.Acp_in2 = rect_Acp_in2
                    self.Pcp_in = rect_Pcp_in
                    self.Torsion_threshold = vc_fprimec_psi**(1/2.0) * area_over_perim_rect
                    self.AoP_status = 'Rectangular Section used for Acp and Pcp, ACI 318-08 11.5.1.1'
                else:
                    self.Acp_in2 = Acp_in2
                    self.Pcp_in = Pcp_in
                    self.Torsion_threshold = vc_fprimec_psi**(1/2.0) * area_over_perim_t
                    self.AoP_status = 'T Section used for Acp and Pcp, Section may have been altered per ACI 318-08 11.5.1.1 and 13.2.4'
            elif self.bf_right_in ==0:
                Torsion_bf_left_in = min(self.bf_left_in, self.hw_in, 4*self.hf_in)
                Acp_in2 = (self.bw_in*self.hw_in) + ((self.bw_in+Torsion_bf_left_in)*self.hf_in)
                Pcp_in = self.bw_in + self.hw_in + Torsion_bf_left_in + self.hf_in + Torsion_bf_left_in + self.bw_in + self.h_in
                
                #Check Acp^2/Pcp of T Beam not less than for Rectangular beam
                area_over_perim_t = (Acp_in2**2.0)/Pcp_in
                
                if area_over_perim_rect > area_over_perim_t:
                    self.Acp_in2 = rect_Acp_in2
                    self.Pcp_in = rect_Pcp_in
                    self.Torsion_threshold = vc_fprimec_psi**(1/2.0) * area_over_perim_rect
                    self.AoP_status = 'Rectangular Section used for Acp and Pcp, ACI 318-08 11.5.1.1'
                else:
                    self.Acp_in2 = Acp_in2
                    self.Pcp_in = Pcp_in
                    self.Torsion_threshold = vc_fprimec_psi**(1/2.0) * area_over_perim_t
                    self.AoP_status = 'T Section used for Acp and Pcp, Section may have been altered per ACI 318-08 11.5.1.1 and 13.2.4'
        else:
            Torsion_bf_right_in = min(self.bf_right_in, self.hw_in, 4*self.hf_in)
            Torsion_bf_left_in = min(self.bf_left_in, self.hw_in, 4*self.hf_in)
            Acp_in2 = (self.bw_in*self.hw_in) + ((self.bw_in+Torsion_bf_left_in+Torsion_bf_right_in)*self.hf_in)
            Pcp_in = self.bw_in + self.hw_in + Torsion_bf_right_in + self.hf_in + Torsion_bf_right_in + self.bw_in + Torsion_bf_left_in + self.hf_in + Torsion_bf_left_in + self.hw_in

            #Check Acp^2/Pcp of T Beam not less than for Rectangular beam
            area_over_perim_t = (Acp_in2**2.0)/Pcp_in
            
            if area_over_perim_rect > area_over_perim_t:
                self.Acp_in2 = rect_Acp_in2
                self.Pcp_in = rect_Pcp_in
                self.Torsion_threshold = vc_fprimec_psi**(1/2.0) * area_over_perim_rect
                self.AoP_status = 'Rectangular Section used for Acp and Pcp, ACI 318-08 11.5.1.1'
            else:
                self.Acp_in2 = Acp_in2
                self.Pcp_in = Pcp_in
                self.Torsion_threshold = vc_fprimec_psi**(1/2.0) * area_over_perim_t
                self.AoP_status = 'T Section used for Acp and Pcp, Section may have been altered per ACI 318-08 11.5.1.1 and 13.2.4'

        return phi, self.Acp_in2, self.Pcp_in, self.Torsion_threshold, phi*self.Torsion_threshold, self.AoP_status
        
    def cracked_moment_of_inertia_in4(self,bars_as_array,bars_d_array,Es_psi):
        self.cmi_c_x = []
        self.cmi_c_y = []
        self.cmi_s_x = []
        self.cmi_s_y = []
        self.cmi_s_text = []
        self.cmi_c_text = []
        n = Es_psi/self.Ec_psi

        a=0
        b=max(bars_d_array)
        c=0
        mna = 0
        self.crackna = 0

        loop_max = 10000
        tol = 0.0000000000001
        loop = 0

        while loop<loop_max:
            c = (a+b)/2

            if c <= self.hf_in:
                compression_block_in2 = self.bf_in * c
                compression_block_cg_top = c/2

            else:
                compression_block_in2 = (self.bf_in * self.hf_in) + (self.bw_in*(c-self.hf_in))
                compression_block_cg_top = (self.Af_in2*(self.hf_in/2.0) + (self.bw_in*(c-self.hf_in))*(((c-self.hf_in)/2.0)+self.hf_in))/compression_block_in2

            mna = compression_block_in2 * compression_block_cg_top
            i=0
            for i in range(len(bars_as_array)):
                if c < bars_d_array[i]:
                    mna = mna - (n*bars_as_array[i]*(bars_d_array[i]-c))
                else:
                    mna = mna + ((n-1)*bars_as_array[i]*(c-bars_d_array[i]))

            if mna == 0 or (b-a)/2 <= tol:
                self.crackna = c
                loop = loop_max
            elif mna > 1:
                b = c
            else:
                a = c
            loop+=1
        if self.crackna <= self.hf_in:
            i_crack_in4 = (self.bf_in*self.crackna**3)/3
            self.cmi_c_x.append([0-self.bf_left_in,0+self.bw_in+self.bf_right_in,0+self.bw_in+self.bf_right_in,0-self.bf_left_in,0-self.bf_left_in])
            self.cmi_c_y.append([self.h_in - self.crackna,self.h_in - self.crackna,self.h_in,self.h_in,self.h_in - self.crackna])
            self.cmi_c_text.append(['Ac = {0:.3f} in2, Ec = {1:.2f} psi, Es = {2:0.2f} psi, n = Es/Ec = {3:0.4f}'.format(compression_block_in2, self.Ec_psi, Es_psi, n),0-self.bf_left_in,self.h_in+0.25])
        else:
            i_crack_in4 = (self.bw_in*(self.crackna-self.hf_in)**3)/3 + (self.bf_in*self.hf_in**3/3) + (self.bf_in*self.hf_in)*(self.crackna-self.hf_in)**2
            self.cmi_c_x.append([0-self.bf_left_in,0-self.bf_left_in,0,0,self.bw_in,self.bw_in,self.bw_in+self.bf_right_in,self.bw_in+self.bf_right_in,0-self.bf_left_in])
            self.cmi_c_y.append([self.h_in,self.hw_in,self.hw_in,self.h_in-self.crackna,self.h_in-self.crackna,self.hw_in,self.hw_in,self.h_in,self.h_in])
            self.cmi_c_text.append(['Ac = {0:.3f} in2, Ec = {1:.2f} psi, Es = {2:0.2f} psi, n = Es/Ec = {3:0.4f}'.format(compression_block_in2, self.Ec_psi, Es_psi, n),0-self.bf_left_in,self.h_in+0.25])
        for i in range(len(bars_as_array)):
            if self.crackna < bars_d_array[i]:
               i_crack_in4 = i_crack_in4 + (n*bars_as_array[i]*(bars_d_array[i]-self.crackna)**2)
               self.cmi_s_x.append([(self.bw_in/2.0)-(n*bars_as_array[i]/2.0),(self.bw_in/2.0)+(n*bars_as_array[i]/2.0),(self.bw_in/2.0)+(n*bars_as_array[i]/2.0),(self.bw_in/2.0)-(n*bars_as_array[i]/2.0),(self.bw_in/2.0)-(n*bars_as_array[i]/2.0)])
               self.cmi_s_y.append([self.h_in - (bars_d_array[i]-0.5),self.h_in - (bars_d_array[i]-0.5),self.h_in - (bars_d_array[i]+0.5),self.h_in - (bars_d_array[i]+0.5),self.h_in - (bars_d_array[i]-0.5)])
               self.cmi_s_text.append(['nAs = {0:.3f} in2'.format(n*bars_as_array[i]),((self.bw_in/2.0)+(n*bars_as_array[i]/2.0))+0.25,self.h_in - (bars_d_array[i]+0.25)])
            else:
                i_crack_in4 = i_crack_in4 + ((n-1)*bars_as_array[i]*(self.crackna-bars_d_array[i])**2)
                self.cmi_s_x.append([(self.bw_in/2.0)-(n*bars_as_array[i]/2.0),(self.bw_in/2.0)+(n*bars_as_array[i]/2.0),(self.bw_in/2.0)+(n*bars_as_array[i]/2.0),(self.bw_in/2.0)-(n*bars_as_array[i]/2.0),(self.bw_in/2.0)-(n*bars_as_array[i]/2.0)])
                self.cmi_s_y.append([self.h_in - (bars_d_array[i]-0.5),self.h_in - (bars_d_array[i]-0.5),self.h_in - (bars_d_array[i]+0.5),self.h_in - (bars_d_array[i]+0.5),self.h_in - (bars_d_array[i]-0.5)])
                self.cmi_s_x.append([(self.bw_in/2.0)-(bars_as_array[i]/2.0),(self.bw_in/2.0)+(bars_as_array[i]/2.0),(self.bw_in/2.0)+(bars_as_array[i]/2.0),(self.bw_in/2.0)-(bars_as_array[i]/2.0),(self.bw_in/2.0)-(bars_as_array[i]/2.0)])
                self.cmi_s_y.append([self.h_in - (bars_d_array[i]-0.5),self.h_in - (bars_d_array[i]-0.5),self.h_in - (bars_d_array[i]+0.5),self.h_in - (bars_d_array[i]+0.5),self.h_in - (bars_d_array[i]-0.5)])
                self.cmi_s_text.append(['(n-1)As = {0:.3f} in2'.format((n-1)*bars_as_array[i]),((self.bw_in/2.0)+(n*bars_as_array[i]/2.0))+0.25,self.h_in - (bars_d_array[i]+0.25)])
        return i_crack_in4, self.crackna

class ACI_Concrete:
    def __init__(self,f_prime_c_psi,density_pcf):
        
        self.f_prime_c_psi = f_prime_c_psi
        self.f_prime_c_ksi = f_prime_c_psi/1000.0
        
        self.errors = []
        self.warnings = []
        self.error = False
        
        if (90<=density_pcf) and (density_pcf<=115):
            self.weight_class = "Lightweight"
            self.lamba_wc = 0.75
            self.density_pcf = density_pcf
            
        elif (115<density_pcf) and (density_pcf<=160):
            self.weight_class = "Normalweight"
            self.lamba_wc = 1.0
            self.density_pcf = density_pcf
        
        else:
            self.weight_class = "Undefined"
            self.lamba_wc = 0
            self.density_pcf = 0
            self.error = True
            self.errors.append("Density is outside the acceptable range of 90 to 160 pcf")
        
        self.Ec_psi = math.pow(self.density_pcf,1.5)*33.0*math.sqrt(self.f_prime_c_psi)
        self.Ec_kis = self.Ec_psi/1000.0
    
    def modulus_of_rupture(self):
        self.fr_psi = 7.5*self.lamba_wc*math.sqrt(self.f_prime_c_psi)
    
    def lamba_wc_override(self, lamba_wc):
        self.lamba_wc = lamba_wc
    
class Unit_Width_Section:
    def __init__(self,H_in,B_in=12.0):
        
        self.H_in = H_in
        self.B_in = B_in

def aci_beta1(f_prime_c_psi):

    if f_prime_c_psi <= 4000:
        beta1 = 0.85
    elif f_prime_c_psi <= 8000:
        beta1 = 0.85 - ((0.05*(f_prime_c_psi-4000))/1000)
    else:
        beta1 = 0.65
    
    return beta1

def aci_phi(et, ety, ties="Other"):
    
    if et >= 0.005:
        phi = 0.9
        section_classification = "Tension-controlled"
    
    elif et <= ety:
        if ties == "Other":
            phi = 0.65
        else:
            phi = 0.75
        section_classification = "Compression-controlled"
    
    else:
        if ties == "Other":
            phi = 0.65 + (0.25 * ((et - ety)/(0.005-ety)))
        else:
            phi = 0.75 + (0.15 * ((et - ety)/(0.005-ety)))
            
        section_classification = "Transition"
    
    return [phi,section_classification]
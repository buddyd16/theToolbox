# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 15:58:27 2022

@author: DonB
"""

class NDSDatabase:
    def __init__(self):
        filename_table_4a = "wood/static/csv/nds2018_table4a.csv"
        filename_table_4b = "wood/static/csv/nds2018_table4b.csv"

        table_4a = {}
        table_4b = {}

        # Table 4A - Dictionary
        table4a_file = open(filename_table_4a,'r')

        table4a_data_raw = table4a_file.readlines()

        table4a_file.close()

        for line in table4a_data_raw[1:]:
            
            line = line.split(',')
            line[-1] = line[-1].rstrip('\n')
            
            species = line[0]
            grade = line[1]
            size_class = line[2]
            fb_psi = float(line[3])
            ft_psi = float(line[4])
            fv_psi = float(line[5])
            fcp_psi = float(line[6])
            fc_psi = float(line[7])
            e_psi = float(line[8])
            emin_psi = float(line[9])
            g = float(line[10])
            agency = line[11]
            bmin = float(line[12])
            bmax = float(line[13])
            dmin = float(line[14])
            dmax = float(line[15])
            
            ref_vals = {"Fb":fb_psi,"Ft":ft_psi,"Fv":fv_psi,
                        "Fcp":fcp_psi,"Fc":fc_psi,"E":e_psi,
                        "Emin":emin_psi,"G":g}

            if species not in table_4a:
                table_4a[species] = {}
            
            if grade not in table_4a[species]:
                table_4a[species][grade] = {}
            
            if size_class not in table_4a[species][grade]:
                table_4a[species][grade][size_class] = {}
            
            table_4a[species][grade][size_class].update({
                                            "Reference Values": ref_vals, 
                                            "Agency": agency,
                                            "Brange":[bmin,bmax],
                                            "Drange":[dmin,dmax]})
            
        # Table 4B - Dictionary
        table4b_file = open(filename_table_4b,'r')

        table4b_data_raw = table4b_file.readlines()

        table4b_file.close()

        for line in table4b_data_raw[1:]:
            
            line = line.split(',')
            line[-1] = line[-1].rstrip('\n')
            
            species = line[0]
            grade = line[1]
            size_class = line[2]
            fb_psi = float(line[3])
            ft_psi = float(line[4])
            fv_psi = float(line[5])
            fcp_psi = float(line[6])
            fc_psi = float(line[7])
            e_psi = float(line[8])
            emin_psi = float(line[9])
            g = float(line[10])
            agency = line[11]
            bmin = float(line[12])
            bmax = float(line[13])
            dmin = float(line[14])
            dmax = float(line[15])
            
            ref_vals = {"Fb":fb_psi,"Ft":ft_psi,"Fv":fv_psi,
                        "Fcp":fcp_psi,"Fc":fc_psi,"E":e_psi,
                        "Emin":emin_psi,"G":g}

            if species not in table_4b:
                table_4b[species] = {}
            
            if grade not in table_4b[species]:
                table_4b[species][grade] = {}
                
            if size_class not in table_4b[species][grade]:
                table_4b[species][grade][size_class] = {}
            
            table_4b[species][grade][size_class].update({
                                            "Reference Values": ref_vals, 
                                            "Agency": agency,
                                            "Brange":[bmin,bmax],
                                            "Drange":[dmin,dmax]})

        self.table_4a = table_4a
        self.table_4b = table_4b

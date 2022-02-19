import steel.welds_elastic_method as elasticWeld
import math

def elastic_weld_analysis(segments, loads, loadpoint, loadtype):
    
    # create the individual weld segments
    welds = []
    
    count = 1 
    for segment in segments:
        
        i = [segment[0],segment[1]]
        j = [segment[2],segment[3]]
        
        welds.append(elasticWeld.weld_segment(i,j,count))
        
        count += 1
    
    # Create the weld group
    weld_group = elasticWeld.elastic_weld_group(welds)
    
    # Force Analysis
    if loadpoint[0]=="centroid":
        
        fz = loads[0]*1000
        fx = loads[1]*1000
        fy = loads[2]*1000
        mx = loads[3]*1000*12
        my = loads[4]*1000*12
        tz = loads[5]*1000*12
        
        appliedLoad = [fz,fx,fy,mx,my,tz]
        
        sigma_psi = weld_group.force_analysis(fz,fx,fy,mx,my,tz)
    
    else:
        # load point is not at the weld centroid
        x = loadpoint[1][0]
        y = loadpoint[1][1]
        z = loadpoint[1][2]
        
        # distance from user load to load point
        dx = x - weld_group.Cx
        dy = y - weld_group.Cy
        dz = z
    
        fz = loads[0]*1000
        fx = loads[1]*1000
        fy = loads[2]*1000
        mx = loads[3]*1000*12
        my = loads[4]*1000*12
        tz = loads[5]*1000*12
    
        mxx = mx - (fy*dz)+(fz*dy)
        myy = my + (fx*dz)-(fx*dx)
        tzz = tz - (fx*dy)+(fy*dx)
        
        appliedLoad = [fz,fx,fy,mxx,myy,tzz]
        
        sigma_psi = weld_group.force_analysis(fz,fx,fy,mxx,myy,tzz)
    
    #print(sigma_psi)
    
    return welds, weld_group, sigma_psi, appliedLoad

def fillet_weld(sigma_psi,fexx, sigma_type):
    
    if sigma_type == "service":
        reduction = 2
        rn_req = (sigma_psi/1000)*reduction
        #math.append(f"\[\frac{{\sigma}}{{1000}}\cdot\Omega \]")
        throat = rn_req/(0.6*fexx)
        #math.append(f"\[\frac{{R_{{n,req}}}}{{0.6 \cdot F_{{exx}}}} \]")
        fillet_16 = throat/((math.sqrt(2)/2)/16.0)
        #math.append(f"\[\frac{{16.0 \cdot {throat:.3f}}}{{\frac{{\sqrt{{2}}{{2}}}} \]")
        fillet = math.ceil(fillet_16)
        rn_16 = fillet_16*(math.sqrt(2)/2)*(1/16.0)*(0.6*fexx)
        rn = fillet*(math.sqrt(2)/2)*(1/16.0)*(0.6*fexx)
        #math.append(f"\[{fillet:.3f} \cdot \frac{{\sqrt{{2}}}}{{2}} \cdot \frac{{1}}{{16.0}} \cdot 0.6*F_{{exx}} \]")
    else:
        reduction = 0.75
        rn_req = (sigma_psi/1000)/reduction
        throat = rn_req/(0.6*fexx)
        fillet_16 = throat/((math.sqrt(2)/2)/16.0)
        fillet = math.ceil(fillet_16)
        rn_16 = fillet_16*(math.sqrt(2)/2)*(1/16.0)*(0.6*fexx)
        rn = fillet*(math.sqrt(2)/2)*(1/16.0)*(0.6*fexx)
    
    return [reduction,rn_req,throat,fillet_16,rn_16, fillet, rn]
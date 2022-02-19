import general.section_props as sectionprops
import math


def linear_interpolate(x1,x2,x,y1,y2):
    
    x1 = float(x1)
    x2 = float(x2)
    x = float(x)
    y1 = float(y1)
    y2 = float(y2)
    
    if min(x1,x2) < x and max(x1,x2) > x:
    
        if (x2-x1)==0:
            y=0
        else:
            y = y1+((y2-y1)*((x-x1)/(x2-x1)))
        
        return [y,1]
    
    else:
        return ["x must be between x1 and x2",0]
        

def sectionProps(x,y):
    
    x=[float(i) for i in x]
    y=[float(j) for j in y]
    
    shape = sectionprops.Section(x,y)
    
    web_output = []
    web_warnings = shape.warnings
    
    
    for i,j in zip(shape.output,shape.output_strings):
        if type(i) is str:
            web_output.append('{1} = {0}'.format(i,j))
        else:
            web_output.append('{1} = {0:.3f}'.format(i,j))
    
    centroid_web = f'{{x: {shape.cx}, y: {shape.cy}}}'
    
    return web_output,web_warnings, centroid_web, shape


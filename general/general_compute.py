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
        

def sectionProps(sections):

    # NEW STUFF HERE
    shapes = []
    composite = sectionprops.Composite_Section()

    for i,section in enumerate(sections):
        x = section["X"]
        y = section["Y"]
        e = section["E"]
        fy = section["Fy"]
        if section["Solid"] == 1:
            solid = True
        else:
            solid = False

        if i == 0:
            modRatio = 1
        else:
            modRatio = e / sections[0]["E"]
            print(e)
            print(sections[0]["E"])
            print(modRatio)

        shapes.append(sectionprops.Section(x,y,solid,n=modRatio,E=e,Fy=fy))
        print(shapes[-1])
        composite.add_section(shapes[-1])
    
    composite.calculate_properties()
    basefy = sections[0]["Fy"]

    Zx = composite.plastic_Zx(baseFy = basefy)
    Zy = composite.plastic_Zy(baseFy = basefy)
    Zu = composite.plastic_Zu(baseFy = basefy)
    Zv = composite.plastic_Zv(baseFy = basefy)

    # END NEW STUFF
    
    return (composite, shapes)


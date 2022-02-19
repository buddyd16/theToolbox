function linear_interpolate(x1,y1,x2,y2,x){

    let y=0;

    if(Math.min(x1,x2) < x && Math.max(x1,x2) > x){
        if((x2-x1)==0){
            y=0
        } else {
            y = y1+((y2-y1)*((x-x1)/(x2-x1)))
        };

        return [y,1]
        
    } else{

        return ["x must be between x1 and x2",0]
    };

};

function bilinear_interpolate(x1,y1,x2,y2,x,y,f11,f12,f21,f22){
    
    /*
    xi - x values at start and end of x range
    x -  x value at location of interest
    yi - y values at start and end of y range
    y - y value at location of interest
    f11 - function value at (x1,y1)
    f12 - function value at (x1,y2)
    f21 - function value at (x2,y1)
    f22 - function value at (x2,y2)
    */

    let fxy =  0;
    let fxy1 = 0;
    let fxy2 = 0;
    let fx1y = 0;
    let fx2y = 0;

    if((x2-x1)==0 ||(y2-y1)==-0){
        //If x2 - x1 = 0 or y2-y1 = 0, then f is a line
        //Assume this isn't what the user intended and just return an error
        //Rather than performing further checks to do a linear interpolation
        //linear interpolation could only be done if the function vertex pairs
        //where the same values, otherwise the data is invalid since the function
        //can't have two values at the same point.
        return ["(x1,y1) and (x2,y2) lie on the same plane",[0,0,0,0],0]
        
    } else if(Math.min(x1,x2) < x && Math.max(x1,x2) > x && Math.min(y1,y2)<y && Math.max(y1,y2) > y){

            fxy1 = (((x2-x)/(x2-x1))*f11)+(((x-x1)/(x2-x1))*f21);
            fxy2 = (((x2-x)/(x2-x1))*f12)+(((x-x1)/(x2-x1))*f22);
            fxy = (((y2-y)/(y2-y1))*fxy1)+(((y-y1)/(y2-y1))*fxy2);

            fx1y = linear_interpolate(y1,f11,y2,f12,y)[0];
            fx2y = linear_interpolate(y1,f21,y2,f22,y)[0];

            return [fxy,[fx1y,fx2y,fxy1,fxy2],1]
        
    } else {

        return ["(x,y) must be between (x1,y1) and (x2,y2)",[0,0,0,0],0]
    };
}

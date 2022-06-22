
function writeTemplateResults(x,y,shapestrg){

    let verticestable = '';

    // Loop through vertices
    x.forEach(function(item, index){

        if (index == 0){
            verticestable += '<tr class=\"user vertex\">' +
                        '<td>'+(index+1)+'</td>' +
                        '<td><input id=\"'+ shapestrg +'firstX\" name=\"'+ shapestrg +'x\" class=\"'+ shapestrg +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+x[index]+'\" onchange=first_to_last(\"'+ shapestrg +'\");></td>' +
                        '<td><input id=\"'+ shapestrg +'firstY\" name=\"'+ shapestrg +'y\" class=\"'+ shapestrg +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+y[index]+'\" onchange=first_to_last(\"'+ shapestrg +'\");></td>' +
                        '</tr>'
        } else if (index == 1){
            verticestable += '<tr class=\"user vertex\">' +
                        '<td>'+(index+1)+'</td>' +
                        '<td><input name=\"'+ shapestrg +'x\" class=\"'+ shapestrg +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+x[index]+'\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
                        '<td><input name=\"'+ shapestrg +'y\" class=\"'+ shapestrg +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+y[index]+'\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
                        '</tr>'
        } else if (index == 2){
            verticestable += '<tr class=\"user vertex\">' +
                        '<td>'+(index+1)+'</td>' +
                        '<td><input name=\"'+ shapestrg +'x\" class=\"'+ shapestrg +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+x[index]+'\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
                        '<td><input name=\"'+ shapestrg +'y\" class=\"'+ shapestrg +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+y[index]+'\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
                        '<td>' +
                        '<button type=\"button\" onclick=addFirstVertexRow(\"'+ shapestrg +'\"); class=\"btn btn-secondary btn-success btn-sm\">' +
                        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                        '</svg>' +
                        '</button>' +
                        '</td>' +
                        '</tr>'
        } else if (index+1 == x.length){
            verticestable += '<tr class=\"vertex\">' +
                        '<td>Close</td>' +
                        '<td><input id=\"'+ shapestrg +'lastX\" name=\"'+ shapestrg +'x\" class=\"'+ shapestrg +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+x[index]+'\" readonly></td>' +
                        '<td><input id=\"'+ shapestrg +'lastY\" name=\"'+ shapestrg +'y\" class=\"'+ shapestrg +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+y[index]+'\" readonly></td>' +
                        '</tr>'
        } else {
            verticestable += '<tr class=\"user vertex\">' +
            '<td>' + (index+1) + '</td>' +
            '<td><input name=\"'+ shapestrg +'x\" class=\"'+ shapestrg +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+x[index]+'\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
            '<td><input name=\"'+ shapestrg +'y\" class=\"'+ shapestrg +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"'+y[index]+'\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
            '<td>' +
            '<button type=\"button\" onclick=addVertexRow(this,\''+ shapestrg +'\'); class=\"btn btn-secondary btn-success btn-sm\">' +
            '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
            '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
            '</svg>' + 
            '</button>' +
            '<a href=\"#\" onclick=\"removeVertexRow(this,\''+ shapestrg +'\'); return false;\" class=\"badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
            '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
            '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
            '</svg></a></td>' +
            '</tr>'
        }

    });

    $('#'+ shapestrg +'vertexTableBody').html(verticestable);
    modelRun = 0;

    areaAndCentroid(shapestrg);

};

function rectangle(){

    let shapestrg = $('#templateSelectedShape').val();
    let B = Number($('#templateRectangleB').val());
    let H = Number($('#templateRectangleH').val());

    let x = [0,B,B,0,0];
    let y = [0,0,H,H,0];

    writeTemplateResults(x,y,shapestrg);
};

function threePointBezierCurve(p1,p2,p3,segments){
    let x = [];
    let y = [];
    let p1x = p1[0];
    let p1y = p1[1];
    let p2x = p2[0];
    let p2y = p2[1];
    let p3x = p3[0];
    let p3y = p3[1];

    let t_step = 1/segments;
    let t = 0;

    while (t<1){

        x.push(((1-t)*(((1-t)*p1x)+(t*p2x)))+(t*(((1-t)*p2x)+(t*p3x))));
        y.push(((1-t)*(((1-t)*p1y)+(t*p2y)))+(t*(((1-t)*p2y)+(t*p3y))));

        t += t_step;
    };

    x.push(p3x);
    y.push(p3y);

    return [x,y];
};

function bezierFillet(){

    let shapestrg = $('#templateSelectedShape').val();
    let B = Number($('#templateParaFilletB').val());
    let H = Number($('#templateParaFilletH').val());

    let x = [0];
    let y = [0];
    let p1x = B;
    let p1y = 0;
    let p2x = 0;
    let p2y = 0;
    let p3x = 0;
    let p3y = H;

    let bezier = threePointBezierCurve([p1x,p1y],[p2x,p2y],[p3x,p3y],50);

    x.push(...bezier[0]);
    y.push(...bezier[1]);

    x.push(0);
    y.push(0);

    writeTemplateResults(x,y,shapestrg);
};

function flatbaseTrapezoid(){
    let shapestrg = $('#templateSelectedShape').val();
    let B = Number($('#templateTrapB').val());
    let H1 = Number($('#templateTrapH1').val());
    let H2 = Number($('#templateTrapH2').val());

    let x = [0,B,B,0,0];
    let y = [0,0,H2,H1,0];

    writeTemplateResults(x,y,shapestrg);
};

function rightTriangle(){
    let shapestrg = $('#templateSelectedShape').val();
    let B = Number($('#templateRTriangleB').val());
    let H = Number($('#templateRTriangleH').val());

    let x = [0,B,0,0];
    let y = [0,0,H,0];

    writeTemplateResults(x,y,shapestrg);
};

function generalTriangle(){
    let shapestrg = $('#templateSelectedShape').val();
    let a = Number($('#templateGTriangleS1').val());
    let b = Number($('#templateGTriangleS2').val());
    let c = Number($('#templateGTriangleS3').val());

    let s = (a+b+c)/2;
    let area = Math.sqrt(s*(s-a)*(s-b)*(s-c));
    let z = (2*area)/a;
    let w = Math.sqrt((c*c)-(z*z));

    let x = [0,a,w,0];
    let y = [0,0,z,0];

    writeTemplateResults(x,y,shapestrg);
};

function steelShapeTemplate(){
    let shapestrg = $('#templateSelectedShape').val();
    let shapeset = $('#templateSteelShapeSet').find(":selected").val();
    let shape = $('#templateSteelShapeList').find(":selected").val();
    let units = $('input[name="units"]:checked').val();
    let conversion = 1;

    if (units != "imperial"){
        conversion = 25.4;
    };

    $.ajax({
        url: "/steel/steeldbapi",
        type: "GET",
        dataType: "json",
        data:{"shapeset": shapeset, "shape": shape},

        success: function(shapedata){
            
            console.log(shapedata);
            console.log(shapeset);
            if (shapeset == "WF"){
                let d = Number(shapedata["d"][0])*conversion;
                let bf = Number(shapedata["bf"][0])*conversion;
                let tf = Number(shapedata["tf"][0])*conversion;
                let tw = Number(shapedata["tw"][0])*conversion;
                let k = Number(shapedata["kdes"][0])*conversion;

                //coords = steelWF(d,bf,tf,tw,k);
                coords = steelWFbezierfillets(d,bf,tf,tw,k);

                writeTemplateResults(coords[0],coords[1],shapestrg);
            } else if (shapeset == "WT"){
                let d = Number(shapedata["d"][0])*conversion;
                let bf = Number(shapedata["bf"][0])*conversion;
                let tf = Number(shapedata["tf"][0])*conversion;
                let tw = Number(shapedata["tw"][0])*conversion;
                let k = Number(shapedata["kdes"][0])*conversion;

                coords = steelWT(d,bf,tf,tw,k);

                writeTemplateResults(coords[0],coords[1],shapestrg);
            } else if (shapeset == "L"){
                let d = Number(shapedata["d"][0])*conversion;
                let b = Number(shapedata["b"][0])*conversion;
                let t = Number(shapedata["t"][0])*conversion;
                let k = Number(shapedata["kdes"][0])*conversion;

                coords = steelL(d,b,t,k);

                writeTemplateResults(coords[0],coords[1],shapestrg); 
            };

        },
        error: function(error){
            console.log("Error:");
            console.log(error);
        }
    });
};

function circle_coordinates(x,y,r,start,end){

    // given a center point x,y
    // and a radius
    // return the x,y coordinate list for a circle
    
    let x_out = [];
    let y_out = [];

    let a1 = degreesToRadians(start);
    let a2 = degreesToRadians(end);
    let a_step = degreesToRadians(1);
    

    while (a1 <= a2){
        let x0 = r*Math.cos(a1);
        let y0 = r*Math.sin(a1);
        
        x_out.push(x0+x);
        y_out.push(y0+y);

        a1 += a_step;
    };

    return [x_out,y_out];
};

function steelWFbezierfillets(d,bf,tf,tw,k){
    let segs = 50;

    // # Bottom flange
    let x = [0,bf,bf];
    let y = [0,0,tf];

    // Bottom Right Fillet
    let p1x = (bf/2)+(tw/2)+(k-tf);
    let p1y = tf;
    let p2x = (bf/2)+(tw/2);
    let p2y = p1y;
    let p3x = p2x;
    let p3y = k;

    let bezier = threePointBezierCurve([p1x,p1y],[p2x,p2y],[p3x,p3y],segs);

    x.push(...bezier[0]);
    y.push(...bezier[1]);

    // Top Right Fillet
    p1x = (bf/2)+(tw/2);
    p1y = d-k;
    p2x = p1x;
    p2y = d-tf;
    p3x = (bf/2)+(tw/2)+(k-tf);
    p3y = p2y;

    bezier = threePointBezierCurve([p1x,p1y],[p2x,p2y],[p3x,p3y],segs);

    x.push(...bezier[0]);
    y.push(...bezier[1]);

    x.push(bf);
    y.push(d-tf);
    
    x.push(bf);
    y.push(d);
    
    x.push(0);
    y.push(d);

    x.push(0);
    y.push(d-tf);

    // Top Left Fillet
    p1x = (bf/2)-(tw/2)-(k-tf);
    p1y = d-tf;
    p2x = (bf/2)-(tw/2);
    p2y = p1y;
    p3x = p2x;
    p3y = d-k;

    bezier = threePointBezierCurve([p1x,p1y],[p2x,p2y],[p3x,p3y],segs);

    x.push(...bezier[0]);
    y.push(...bezier[1]);

    // Bottom Left Fillet
    p1x = (bf/2)-(tw/2);
    p1y = k;
    p2x = (bf/2)-(tw/2);
    p2y = tf;
    p3x = (bf/2)-(tw/2)-(k-tf);
    p3y = tf;

    bezier = threePointBezierCurve([p1x,p1y],[p2x,p2y],[p3x,p3y],segs);

    x.push(...bezier[0]);
    y.push(...bezier[1]);

    x.push(0);
    y.push(tf);

    x.push(0);
    y.push(0);

    return [x,y];
};

function steelWF(d,bf,tf,tw,k){

    // # Bottom flange
    let x = [0,bf,bf];
    let y = [0,0,tf];
    
    // # points in bottom right radius angle range is 270,180
    let cr1x = (bf/2.0)+(tw/2.0)+(k-tf);
    let cr1y = k;
    
    // # draw circle for radius in clockwise order then reverse it
    // # for the first radius
    let r=k-tf;
    let r1 = circle_coordinates(cr1x,cr1y,r,180,270);

    r1[0].reverse();
    r1[1].reverse();
    
    x.push(...r1[0]);
    y.push(...r1[1]);

    // # points in top right radius angle range is 180,90
    let cr2x = cr1x;
    let cr2y = d-k;
    
    // # draw circle for radius in clockwise order then reverse it
    // # for the first radius
    let r2 = circle_coordinates(cr2x,cr2y,r,90,180);
    
    r2[0].reverse();
    r2[1].reverse();
    
    x.push(...r2[0]);
    y.push(...r2[1]);
    
    // # top flange
    x.push(...[bf,bf,0,0]);   
    y.push(...[d-tf,d,d,d-tf]);

    // # points in top left radius angle range is 90,0
    let cr3x = (bf/2.0)-(tw/2.0)-(k-tf);
    let cr3y = d-k;
    
    // # draw circle for radius in clockwise order then reverse it
    // # for the first radius
    let r3 = circle_coordinates(cr3x,cr3y,r,0,90);
    
    r3[0].reverse();
    r3[1].reverse();
    
    x.push(...r3[0]);
    y.push(...r3[1]);

    // # points in bottom left radius angle range is 360,270
    let cr4x = cr3x;
    let cr4y = k;
    
    // # draw circle for radius in clockwise order then reverse it
    // # for the first radius
    let r4 = circle_coordinates(cr4x,cr4y,r,270,360);
    
    r4[0].reverse();
    r4[1].reverse();
    
    x.push(...r4[0]);
    y.push(...r4[1]);
    
    // # Last points to close the bottom flange
    x.push(...[0,0]);
    y.push(...[tf,0]);

    return [x,y];
};

function steelWT(d,bf,tf,tw,k){

    // # Bottom flange
    let x = [0,bf,bf];
    let y = [0,0,tf];
    
    // # points in bottom right radius angle range is 270,180
    let cr1x = (bf/2.0)+(tw/2.0)+(k-tf);
    let cr1y = k;
    
    // # draw circle for radius in clockwise order then reverse it
    // # for the first radius
    let r=k-tf;
    let r1 = circle_coordinates(cr1x,cr1y,r,180,270);

    r1[0].reverse();
    r1[1].reverse();
    
    x.push(...r1[0]);
    y.push(...r1[1]);
  
    // # top of web
    let tw_right = (bf/2.0)+(tw/2.0);
    let tw_left = tw_right - tw;

    x.push(...[tw_right,tw_left]);   
    y.push(...[d,d]);

    // # points in bottom left radius angle range is 360,270
    let cr4x = (bf/2.0)-(tw/2.0)-(k-tf);
    let cr4y = k;
    
    // # draw circle for radius in clockwise order then reverse it
    // # for the first radius
    let r4 = circle_coordinates(cr4x,cr4y,r,270,360);
    
    r4[0].reverse();
    r4[1].reverse();
    
    x.push(...r4[0]);
    y.push(...r4[1]);
    
    // # Last points to close the bottom flange
    x.push(...[0,0]);
    y.push(...[tf,0]);

    return [x,y];
};

function steelL(vleg, hleg, thickness, k){
    // given the defining geometric
    // properties for an Angle from
    // AISC
    // return a Shape with appropriate
    // coordinates
    // 0,0 point will be the bottom left of the section

    let r1 = k - thickness; // leg-to-leg Fillet
    let r2 = r1/2.0;        // toe fillet 1/2*Fillet per ISO 657-1: 1989 (E)
    console.log(r1);
    console.log(r2);

    // Bottom horizontal leg
    let x = [0,hleg,hleg];
    let y = [0,0,(thickness - r2)];
    
    console.log(x);
    console.log(y);
    // outisde horizontal leg fillet
    // for the first radius
    let r = r2;
    let fillet1 = circle_coordinates((hleg-r2),(thickness - r2),r,1,90);
    
    x.push(...fillet1[0]);
    y.push(...fillet1[1]);
    
    // horizontal top flat   
    x.push(k);
    y.push(thickness);
    
    //interior corner radii    
    r = r1;
    let fillet2 = circle_coordinates(k,k,r,180,269);
    
    fillet2[0].reverse();
    fillet2[1].reverse();
    
    x.push(...fillet2[0]);
    y.push(...fillet2[1]);
    
    // vertical inside flat
    x.push(thickness);
    y.push((vleg - r2));
    
    // outside vertical leg fillet
    r = r2;
    let fillet3 = circle_coordinates(thickness - r2,vleg-(r2),r,1,90)
    
    x.push(...fillet3[0]);
    y.push(...fillet3[1]);
    
    x.push(0)
    y.push(vleg)
    
    x.push(0)
    y.push(0)

    return [x,y];
};
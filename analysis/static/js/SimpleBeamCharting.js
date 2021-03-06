function UpdateChart(){
    // Get the canvas element size
    var canvas = document.getElementById("bmCanvas");
    var canvas_x = canvas.width;
    var canvas_y = canvas.height;
    var ctx = canvas.getContext("2d");

    // Clear the Canvas
    ctx.clearRect(0,0,canvas_x, canvas_y);

    // beam y and i,j
    var x_margin = 20;
    var beam_y = canvas.height-67;
    var beam_i = x_margin;
    var beam_j = canvas.width-x_margin;
    var beam_span_px = beam_j-beam_i;
    var support_top = beam_y+3;
    var support_bottom = beam_y+33;
    var support_height = support_bottom-support_top;

    // determine the overall beam span length
    // and determine the scale factor for the canvas
    // x coordinates
    var main_span_ft = Number($("#span").val());
    var cant_left_ft = Number($("#overhangLeft").val());
    var cant_right_ft = Number($("#overhangRight").val());
    var total_span_ft = main_span_ft+cant_left_ft+cant_right_ft;
    var x_scale = beam_span_px/total_span_ft;

    //Draw the beam
    ctx.beginPath();
    ctx.lineWidth=6;
    ctx.moveTo(beam_i,beam_y);
    ctx.lineTo(beam_j,beam_y);
    ctx.stroke();

    // Dimension the beam span
    let span_tick_top = beam_y + 35;
    let span_tick_bottom = span_tick_top + 20;
    let span_dim = span_tick_bottom - 10;
    let span_dim_text = total_span_ft.toFixed(3).toString()+" ft";
    
    let chart_units = $('input[name="units"]:checked').val();
    console.log(chart_units);
    
    if( chart_units == "metric"){
        span_dim_text = total_span_ft.toFixed(3).toString()+" m";
    }
    
    let span_mid = ((beam_j-beam_i)/2) + x_margin;
    let span_text_y = span_dim + 18;

    ctx.beginPath();
    ctx.lineWidth=1;
    ctx.moveTo(beam_i, span_tick_top);
    ctx.lineTo(beam_i, span_tick_bottom);
    ctx.stroke();

    ctx.beginPath();
    ctx.lineWidth=1;
    ctx.moveTo(beam_j, span_tick_top);
    ctx.lineTo(beam_j, span_tick_bottom);
    ctx.stroke();

    ctx.beginPath();
    ctx.lineWidth=1;
    ctx.moveTo(beam_i, span_dim);
    ctx.lineTo(beam_j, span_dim);
    ctx.stroke();

    // label the line
    ctx.font = 'bold 18px serif';
    ctx.textAlign = "center";
    ctx.fillText(span_dim_text, span_mid, span_text_y);

    //Draw Left Support
    if ($('#fixedLeft').is(":checked"))
    {
        var supp_left_fix_x = beam_i;
        var supp_left_fix_base = beam_y - 33;
        var supp_left_fix_top = beam_y + 33;

        ctx.beginPath();
        ctx.lineWidth=6;
        ctx.moveTo(supp_left_fix_x,supp_left_fix_base);
        ctx.lineTo(supp_left_fix_x,supp_left_fix_top);
        ctx.stroke();

    } else {
        var supp_left_x1 = (x_scale*cant_left_ft)+x_margin;
        var supp_left_x2 = supp_left_x1-15;
        var supp_left_x3 = supp_left_x1+15;

        ctx.beginPath();
        ctx.lineWidth=1;
        ctx.moveTo(supp_left_x1,support_top);
        ctx.lineTo(supp_left_x2,support_bottom);
        ctx.lineTo(supp_left_x3,support_bottom);
        ctx.fill();
    };

    //Draw Right Support
    if ($('#fixedRight').is(":checked"))
    {
        var supp_right_fix_x = beam_j;
        var supp_right_fix_base = beam_y - 33;
        var supp_right_fix_top = beam_y + 33;

        ctx.beginPath();
        ctx.lineWidth=6;
        ctx.moveTo(supp_right_fix_x,supp_right_fix_base);
        ctx.lineTo(supp_right_fix_x,supp_right_fix_top);
        ctx.stroke();

    } else {
        var supp_right_x = (x_scale*(total_span_ft-cant_right_ft))+x_margin;
        var supp_radius = support_height/2;
        var supp_right_y = support_top + supp_radius;

        ctx.beginPath();
        ctx.arc(supp_right_x,supp_right_y,supp_radius,0,2*Math.PI);
        ctx.fill();
    };

    //Draw Interior Supports
    var int_supports = $(".interiorSupport");

    for(var i = 0; i < int_supports.length; i++){

        var x_ft = Number($(int_supports[i]).val());

        if(x_ft !=0 && x_ft>0 && x_ft<main_span_ft){
            var supp_x = (x_scale*(cant_left_ft+x_ft))+x_margin;
            var supp_radius = support_height/2;
            var supp_right_y = support_top + supp_radius;
            
            ctx.beginPath();
            ctx.arc(supp_x,supp_right_y,supp_radius,0,2*Math.PI);
            ctx.fill();
        };

    };

    //Distributed loads
    var w1s = $("input.w1").map(function(){
        return Number($(this).val());
    }).get();

    var w1t = $("input.trib1").map(function(){
        return Number($(this).val());
    }).get();

    var w2s = $("input.w2").map(function(){
        return Number($(this).val());
    }).get();

    var w2t = $("input.trib2").map(function(){
        return Number($(this).val());
    }).get();

    var dist_a = $("input.dista").map(function(){
        return Number($(this).val());
    }).get();

    var dist_b = $("input.distb").map(function(){
        return Number($(this).val());
    }).get();

    var dist_type = $("select.distloadType").map(function(){
        return $(this).val();
    }).get();

    // Point load data
    var p_p = $("input.pointLoad").map(function(){
        return Number($(this).val());
    }).get();

    var p_a = $("input.pointLoada").map(function(){
        return Number($(this).val());
    }).get();

    var p_type = $("select.pointloadType").map(function(){
        return $(this).val();
    }).get();

    // Point moment data
    var m_m = $("input.pointMoment").map(function(){
        return Number($(this).val());
    }).get();

    var m_a = $("input.pointMomenta").map(function(){
        return Number($(this).val());
    }).get();

    var m_type = $("select.pointMomentType").map(function(){
        return $(this).val();
    }).get();

    let distloads = [];
    let pointloads = [];
    let pointmoments = [];
    let appliedtypes = [];

    // max value holders
    let maxw = 0;
    let maxp = 0;
    let maxm = 0;

    // aggregate dist loads
    for(i = 0; i<w1s.length; i++){
        let w1 = w1s[i]*w1t[i];
        let w2 = w2s[i]*w2t[i];

        maxw = Math.max(maxw,Math.abs(w1),Math.abs(w2));

        console.log(w1 == 0 && w2 == 0);

        if ( w1 == 0 && w2 == 0 ) {

        } else {

            distloads.push([w1,w2,dist_a[i],dist_b[i],dist_type[i]]);

            if(!_.contains(appliedtypes,dist_type[i])){
                appliedtypes.push(dist_type[i])
            }
        }

    };

    // aggregate point loads
    for(i = 0; i<p_p.length; i++){
        let p = p_p[i];

        maxp = Math.max(maxp,Math.abs(p));

        if ( p == 0 ) {

        } else {

            pointloads.push([p,p_a[i],p_type[i]]);

            if(!_.contains(appliedtypes,p_type[i])){
                appliedtypes.push(p_type[i])
            }
        }

    };

    // aggregate point moments
    for(i = 0; i<m_m.length; i++){
        let m = m_m[i];

        maxm = Math.max(maxm,Math.abs(m));

        if ( m == 0 ) {

        } else {

            pointmoments.push([m,m_a[i],m_type[i]]);

            if(!_.contains(appliedtypes,m_type[i])){
                appliedtypes.push(m_type[i])
            }
        }

    };

    let num_types = appliedtypes.length;

    let hload = 320/num_types;
    hload = Math.min(hload,50);

    let dist_y_scale = hload/maxw;
    let p_y_scale =  hload/maxp;
    let m_scale = Math.min(hload,40)/maxm;

    // start y pixel for each load type
    let loadtypey = []
    for(i = 0; i<appliedtypes.length; i++){
        // start y pixel coordinate for each load
        // type.
        loadtypey.push(330-(i*hload)-(i));
        console.log(loadtypey);
    }

    // draw and label the load lines
    for(i = 0; i<appliedtypes.length; i++){
        let label = appliedtypes[i]
        let x1 = 2;
        let x2 = 998;
        let y = loadtypey[i];

        ctx.beginPath();
        ctx.lineWidth=1;
        ctx.setLineDash([15,10]);
        ctx.moveTo(x1,y);
        ctx.lineTo(x2,y);
        ctx.stroke();

        // label the line
        ctx.font = '12px serif';
        ctx.textAlign = "left";
        ctx.fillText(label, x1+2, y-2, 12);

        // rest to solid lines for later
        ctx.setLineDash([]);
    }

    let globalloads = ['D','F','L','H','Lr','S','R','Wx','Wy','Ex','Ey'];
    let colormap = ["rgba(44,62,80,0.5)",
                    "rgba(127,140,141,0.5)",
                    "rgba(169,50,38,0.5)",
                    "rgba(243,156,18,0.5)",
                    "rgba(231,76,60,0.5)",
                    "rgba(123,125,125,0.5)",
                    "rgba(22,160,133,0.5)",
                    "rgba(41,128,185,0.5)",
                    "rgba(52,152,219,0.5)",
                    "rgba(125,60,152,0.5)",
                    "rgba(155,89,182,0.5)"];
    
    let colormapalt = ["rgba(44,62,80,0.8)",
                        "rgba(127,140,141,0.8)",
                        "rgba(169,50,38,0.8)",
                        "rgba(243,156,18,0.8)",
                        "rgba(231,76,60,0.8)",
                        "rgba(123,125,125,0.8)",
                        "rgba(22,160,133,0.8)",
                        "rgba(41,128,185,0.8)",
                        "rgba(52,152,219,0.8)",
                        "rgba(125,60,152,0.8)",
                        "rgba(155,89,182,0.8)"];

    // draw the dist loads
    for(i = 0; i<distloads.length; i++){
        // get the load type index for this load
        let thisloadindex = _.indexOf(appliedtypes,distloads[i][4]);
        let indexforcolor = _.indexOf(globalloads,distloads[i][4]);
        let thiscolor = colormap[indexforcolor];

        let y1 = loadtypey[thisloadindex];
        let y2 = y1 - (dist_y_scale*distloads[i][0]);
        let y3 = y1 - (dist_y_scale*distloads[i][1]);
        let x1 = x_margin + (x_scale*distloads[i][2]);
        let x2 = x_margin + (x_scale*distloads[i][3]);

        ctx.fillStyle = thiscolor;
        ctx.beginPath();
        ctx.lineWidth=1;
        ctx.moveTo(x1,y1);
        ctx.lineTo(x1,y2);
        ctx.lineTo(x2,y3);
        ctx.lineTo(x2,y1);
        ctx.lineTo(x1,y1);
        ctx.stroke();
        ctx.fill();

        ctx.fillStyle = "rgb(0,0,0)";
    }

    // draw point loads
    for(i = 0; i<pointloads.length; i++){
        // get the load type index for this load
        let thisloadindex = _.indexOf(appliedtypes,pointloads[i][2]);
        let indexforcolor = _.indexOf(globalloads,pointloads[i][2]);
        let thiscolor = colormapalt[indexforcolor];

        let arrowh = 0.1*(p_y_scale*pointloads[i][0]);

        let y1 = loadtypey[thisloadindex];
        let y2 = y1 - (p_y_scale*pointloads[i][0]);
        let y3 = y1 - arrowh;
        let x1 = x_margin + (x_scale*pointloads[i][1]);
        let x2 = x1 - Math.abs(arrowh);
        let x3 = x1 + Math.abs(arrowh);

        ctx.strokeStyle = thiscolor;
        ctx.beginPath();
        ctx.lineWidth=3;
        ctx.moveTo(x1,y2);
        ctx.lineTo(x1,y1);
        ctx.lineTo(x2,y3);
        ctx.lineTo(x1,y1);
        ctx.lineTo(x3,y3);
        ctx.stroke();

        ctx.strokeStyle = "rgb(0,0,0)";
    }

    // draw point moments
    for(i = 0; i<pointmoments.length; i++){
        // get the load type index for this load
        let thisloadindex = _.indexOf(appliedtypes,pointmoments[i][2]);
        let indexforcolor = _.indexOf(globalloads,pointmoments[i][2]);
        let thiscolor = colormapalt[indexforcolor];

        console.log(thisloadindex);
        let r = Math.abs(m_scale*(0.5*pointmoments[i][0]));
        let arrowh = 0.1*r;

        let y1 = loadtypey[thisloadindex];
        let xc = x_margin + (x_scale*pointmoments[i][1]);

        let a_start =0;
        let a_end = 0;
        let x1 = 0;

        if(pointmoments[i][0] < 0){
            a_start = Math.PI;
            a_end = Math.PI/2;
            x1 = xc - r;
        } else {
            a_start = Math.PI/2;
            a_end = 2*Math.PI;
            x1 = xc + r
        }

        let ya = y1 - arrowh;
        let x2 = x1 - Math.abs(arrowh);
        let x3 = x1 + Math.abs(arrowh);

        ctx.strokeStyle = thiscolor;
        ctx.beginPath();
        ctx.lineWidth=3;
        ctx.arc(xc,y1,r,a_start,a_end);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(x2,ya);
        ctx.lineTo(x1,y1);
        ctx.lineTo(x3,ya);
        ctx.stroke();

        ctx.strokeStyle = "rgb(0,0,0)";
    }
};
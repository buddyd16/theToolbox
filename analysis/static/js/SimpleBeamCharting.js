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

    //Draw Left Support
    if ($('#fixedLeft').is(":checked"))
    {
        var supp_left_fix_x = beam_i;
        var supp_left_fix_base = beam_y - 40;
        var supp_left_fix_top = beam_y + 40;

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
        var supp_right_fix_base = beam_y - 40;
        var supp_right_fix_top = beam_y + 40;

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

    let maxw = 0;

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
    }).get()

    let distloads = [];
    let appliedtypes = [];

    for(i = 0; i<w1s.length; i++){
        let w1 = w1s[i]*w1t[i];
        let w2 = w2s[i]*w2t[i];

        maxw = Math.max(maxw,Math.abs(w1),Math.abs(w2));

        console.log(w1 == 0 && w2 == 0);

        if ( w1 == 0 && w2 == 0 ) {

        } else {

            distloads.push([w1,w2,dist_a[i],dist_b[i],dist_type[i]]);
            
            console.log(dist_type[i]);
            console.log(!_.contains(appliedtypes,dist_type[i]));

            if(!_.contains(appliedtypes,dist_type[i])){
                appliedtypes.push(dist_type[i])
            }
        }

    };

    console.log(distloads);
    console.log(appliedtypes);
    let num_types = appliedtypes.length;

    let hload = 320/num_types;
    hload = Math.min(hload,50);

    let dist_y_scale = hload/maxw;

    console.log('hload: '+hload)
    console.log(dist_y_scale);

    let loadtypey = []
    for(i = 0; i<appliedtypes.length; i++){
        // start y pixel coordinate for each load
        // type.
        loadtypey.push(330-(i*hload));
    }

    console.log(loadtypey);

    let globalloads = ['D','F','L','H','Lr','S','R','Wx','Wy','Ex','Ey'];
    let colormap = ["rgba(0,51,102,0.3)","rgba(102,255,255,0.3)","rgba(255,51,0,0.3)","rgba(153,102,51,0.3)","rgba(255,102,102)","rgba(204,255,204,0.3)","rgba(51,102,255,0.3)","rgba(255,51,153,0.3)","rgba(255,153,153,0.3)","rgba(0,153,51,0.3)","rgba(102,255,102,0.3)"];

    for(i = 0; i<distloads.length; i++){
        // get the load type index for this load
        let thisloadindex = _.indexOf(appliedtypes,distloads[i][4]);
        let indexforcolor = _.indexOf(globalloads,distloads[i][4]);
        let thiscolor = colormap[indexforcolor];

        console.log((dist_y_scale*distloads[i][0]));
        console.log(loadtypey[thisloadindex]);

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

};
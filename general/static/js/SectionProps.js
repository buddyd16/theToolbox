/* BSD 3-Clause License
Copyright (c) 2022, Donald N. Bockoven III
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
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. */

// Compute the Shape Area and Centroid
function areaAndCentroid(shapestrg){

    let area = 0;
    let cx = 0;
    let cy = 0;

    //Get the X,Y vertices Arrays
    let x = [];
    let y = [];

    //Get all X coordinates
    //Items are found in document order so X,Y pairs should be correct
    $("."+shapestrg+"x").each(function(){
        x.push(Number($(this).val()));
    });

    //Get all Y coordinates
    $("."+shapestrg+"y").each(function(){
        y.push(Number($(this).val()));
    });

    x.forEach(function(item, index){

        if (index < (x.length-1)){
            area += (x[index]*y[index+1])-(x[index+1]*y[index]);
            cx += (x[index]+x[index+1])*((x[index]*y[index+1])-(x[index+1]*y[index]));
            cy += (y[index]+y[index+1])*((x[index]*y[index+1])-(x[index+1]*y[index]));
        }
    });

    area = area/2;
    cx = cx/(6*area);
    cy = cy/(6*area);

    $('#'+shapestrg+'Area').html(area.toFixed(4).toString());
    $('#'+shapestrg+'Xc').html(cx.toFixed(4).toString());
    $('#'+shapestrg+'Yc').html(cy.toFixed(4).toString());

    UpdateChart();

};

function degreesToRadians(degrees){
    return degrees * (Math.PI / 180);
};

//Add a new collapsing card for a new shape
function newshapecard(shapenum){

    let length = "in";
    let stress = "ksi";

    if (units != "imperial"){
        length = "mm";
        stress = "MPa";
    }


    let new_card = '<div class=\"card\" id=\"'+ shapenum +'Card\">' +
                   '<div class=\"card-header\" id=\"'+ shapenum +'Heading\">' +
                   '<h5 class=\"mb-0\">' +
                   '<button type=\"button\" id=\"'+ shapenum +'HeadingButton\" class=\"btn btn-link\" data-toggle=\"collapse\" data-target=\"#'+ shapenum +'Collapse\" aria-expanded=\"flase\" aria-controls=\"'+ shapenum +'Collapse\">' +
                   ''+ shapenum +' Input Data' +
                   '</button>' +
                   '</h5>' +
                   '</div>' +
                   '<div id=\"'+ shapenum +'Collapse\" class=\"collapse\" aria-labelledby=\"'+ shapenum +'Heading\" data-parent=\"#accordion\">' +
                   '<div class=\"card-body\" id=\"'+ shapenum +'Body\">' +
                   '<h6>'+ shapenum +' Properties:</h6>' +
                   '<table id=\"'+ shapenum +'PropsTable\" class=\"table table-sm w-auto\">' +
                   '<tr>' +
                   '<td>Modulus of Elasticity, E</td>' +
                   '<td><input name=\"'+ shapenum +'E\" class=\"input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"29000\"></td>' +
                   '<td class=\"stress_units\">'+ stress +'</td>' +
                   '<tr>' +
                   '<td>Yield Stress: </td>' +
                   '<td><input name=\"'+ shapenum +'Fy\" class=\"input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"36\"></td>' +
                   '<td class=\"stress_units\">'+ stress +'</td>' +
                   '<tr>' +
                   '<td>Void or Solid?</td>' +
                   '<td>' +
                   '<select id=\"'+ shapenum +'VoidSelect\" name=\"'+ shapenum +'Solid\" class=\"input-sm\" style=\"width:95px\" onchange=UpdateChart();>' +
                   '<option value=\"1\"> Solid </option>' +
                   '<option value=\"0\"> Void </option>' +
                   '</select>' +
                   '</td>' +
                   '</tr>' +
                   '<tr>' +
                   '<td>Plot Color</td>' +
                   '<td><input type=\"color\" id=\"'+ shapenum +'Color\" name=\"color\" value=\"#cc0000\" onchange=UpdateChart();></td>' +
                   '</tr>' +
                   '</table>' +
                   '<h6>'+ shapenum +' Vertices:</h6>' +
                   '<table id=\"'+ shapenum +'vertexTable\" class=\"table table-sm w-auto\">' +
                   '<thead>' +
                   '<tr>' +
                   '<th> Vertex ID </th>' +
                   '<th class=\"text-center xvertexheader\"> x (' + length +') </th>' +
                   '<th class=\"text-center yvertexheader\"> y (' + length +') </th>' +
                   '</tr>' +
                   '</thead>' +
                   '<tbody>' +
                   '<tr class=\"user vertex\">' +
                   '<td>1</td>' +
                   '<td><input id=\"'+ shapenum +'firstX\" name=\"'+ shapenum +'x\" class=\"'+ shapenum +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onchange=first_to_last(\"'+ shapenum +'\");></td>' +
                   '<td><input id=\"'+ shapenum +'firstY\" name=\"'+ shapenum +'y\" class=\"'+ shapenum +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onchange=first_to_last(\"'+ shapenum +'\");></td>' +
                   '</tr>' +
                   '<tr class=\"user vertex\">' +
                   '<td>2</td>' +
                   '<td><input name=\"'+ shapenum +'x\" class=\"'+ shapenum +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1.0\" onchange=areaAndCentroid(\"'+ shapenum +'\");></td>' +
                   '<td><input name=\"'+ shapenum +'y\" class=\"'+ shapenum +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0\" onchange=areaAndCentroid(\"'+ shapenum +'\");></td>' +
                   '</tr>' +
                   '<tr class=\"user vertex\">' +
                   '<td>3</td>' +
                   '<td><input name=\"'+ shapenum +'x\" class=\"'+ shapenum +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1\" onchange=areaAndCentroid(\"'+ shapenum +'\");></td>' +
                   '<td><input name=\"'+ shapenum +'y\" class=\"'+ shapenum +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1\" onchange=areaAndCentroid(\"'+ shapenum +'\");></td>' +
                   '<td>' +
                   '<button type=\"button\" onclick=addFirstVertexRow(\"'+ shapenum +'\"); class=\"btn btn-secondary btn-success btn-sm\">' +
                   '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                   '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                   '</svg>' +
                   '</button>' +
                   '</td>' +
                   '</tr>' +
                   '<tr class=\"vertex\">' +
                   '<td>Close</td>' +
                   '<td><input id=\"'+ shapenum +'lastX\" name=\"'+ shapenum +'x\" class=\"'+ shapenum +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" readonly></td>' +
                   '<td><input id=\"'+ shapenum +'lastY\" name=\"'+ shapenum +'y\" class=\"'+ shapenum +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" readonly></td>' +
                   '</tr>' +
                   '</tbody>' +
                   '</table>' +
                   '<h6>Quick Properties</h6>' +
                   '<table class="table table-sm">' +
                   '<tr>' +
                   '<td>Area :</td>' +
                   '<td id="'+ shapenum +'Area"></td>' +
                   '<td class=\"area_units\">' + length +'<sup>2</sup></td>' +
                   '</tr>' +
                   '<tr>' +
                   '<td>x<sub>c</sub></td>' +
                   '<td id="'+ shapenum +'Xc"></td>' +
                   '<td class=\"length_units\">' + length +'</td>' +
                   '</tr>' +
                   '<tr>' +
                   '<td>y<sub>c</sub></td>' +
                   '<td id="'+ shapenum +'Yc"></td>' +
                   '<td class=\"length_units\">' + length +'</td>' +
                   '</tr>' +
                   '</table>' +
                   '<h6>Shape Modifications</h6>'+
                   '<table class=\"table table-sm\">' +
                   '<tr>' +
                   '<td rowspan=\"2\" class=\"text-right align-bottom\">Translation: </td>' +
                   '<td class=\"text-center\">x</td>' +
                   '<td class=\"text-center\">y</td>' +
                   '</tr>' +
                   '<tr>' +
                   '<td><input id=\"translate_'+ shapenum +'_x\" class=\"input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1\"></td>' +
                   '<td><input id=\"translate_'+ shapenum +'_y\" class=\"input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1\"></td>' +
                   '<td><button type=\"button\" onclick=\"translateVertices(\''+ shapenum +'\');\" class=\"btn btn-secondary btn-sm\">Translate</button></td>' +
                   '</tr>' +
                   '<tr>' +
                   '<td rowspan=\"2\" class=\"align-bottom\">Rotation (degrees)<br>Counter-Clockwise Positive</td>' +
                   '<td colspan=\"2\" class=\"text-center\">Center of Rotation</td>' +
                   '</tr>' +
                   '<tr>' +
                   '<td class=\"text-center\">x</td>' +
                   '<td class=\"text-center\">y</td>' +
                   '</tr>' +
                   '<tr>' +
                   '<td><input id=\"rotate_'+ shapenum +'_theta\" class=\"input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                   '<td><input id=\"rotate_'+ shapenum +'_x\" class=\"input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                   '<td><input id=\"rotate_'+ shapenum +'_y\" class=\"input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                   '<td><button type=\"button\" onclick=\"rotateVertices(\''+ shapenum +'\');\" class=\"btn btn-secondary btn-sm\">Rotate</button></td>' +
                   '</tr>' +
                   '</table>' +
                   '</div>' +
                   '</div>' +
                   '</div>'
    
    return new_card;
};

//Function to add the first vertex data row defined by the clicked button
//The first added row allows for the remove method
function addFirstVertexRow(shapestrg) {

    let shapetbl = shapestrg +"vertexTable";

    $("#"+ shapetbl +" tbody tr:last").before(
        '<tr class=\"user vertex\">' +
        '<td>' + Number($("#"+ shapetbl +" tbody tr").length).toString() + '</td>' +
        '<td><input name=\"'+ shapestrg +'x\" class=\"'+ shapestrg +'x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
        '<td><input name=\"'+ shapestrg +'y\" class=\"'+ shapestrg +'y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onchange=areaAndCentroid(\"'+ shapestrg +'\");></td>' +
        '<td>' +
        '<button type=\"button\" onclick=addVertexRow(this,'+ shapestrg +'); class=\"btn btn-secondary btn-success btn-sm\">' +
        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
        '</svg>' + 
        '</button>' +
        '<a href=\"#\" onclick=\"removeVertexRow(this,'+ shapestrg +'); return false;\" class=\"badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
        '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
        '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
        '</svg></a></td>' +
        '</tr>'
        );

};

//Function to add a vertex data row defined by the clicked button
function addVertexRow(btn, shapestrg){
        
    //get the current parent
    var tableBody = $(btn).closest("tbody");
    
    //get the current row
    var $curRow = $(btn).closest("tr");
    
    $newRow = $curRow.clone(true)
    
    $curRow.after($newRow)
    
    //expand function to renumber the remaining vertices
    tableBody.children('.user').each(function(i) {
    // Renumber the row
      $(this).children("td:first").text(String(i+1));
    });
    
    areaAndCentroid(shapestrg);
};

//Function to remove a vertex data row defined by the clicked button
function removeVertexRow(btn, shapestrg){

    //get the current parent
    var tableBody = $(btn).closest("tbody");
    
    //remove the row
    $(btn).closest("tr").remove();
    
    //expand function to renumber the remaining vertices
    tableBody.children('.user').each(function(i) {
    // Renumber the row
        $(this).children("td:first").text(String(i+1));
    });

    areaAndCentroid(shapestrg);
};

//Function to translate a shapes vertices
function translateVertices(shapestrg){

    let xt = Number($("#translate_"+shapestrg+"_x").val());
    let yt = Number($("#translate_"+shapestrg+"_y").val());

    $("."+shapestrg+"x").each(function(){
        let x = Number($(this).val()) + xt;

        $(this).val(x);
    });

    $("."+shapestrg+"y").each(function(){
        let y = Number($(this).val()) + yt;
        
        $(this).val(y);
    });

    areaAndCentroid(shapestrg);
};

//Function to rotate shapes vertices around a defined center point
function rotateVertices(shapestrg){

    let rotation_degrees = Number($("#rotate_"+shapestrg+"_theta").val());
    let xc = Number($("#rotate_"+shapestrg+"_x").val());
    let yc = Number($("#rotate_"+shapestrg+"_y").val());
    let angle = degreesToRadians(rotation_degrees);
    let i = 0;

    let x = [];
    let y = [];

    //Get all X coordinates
    //Items are found in document order so X,Y pairs should be correct
    $("."+shapestrg+"x").each(function(){
        x.push(Number($(this).val()));
    });

    //Get all Y coordinates
    $("."+shapestrg+"y").each(function(){
        y.push(Number($(this).val()));
    });

    //Perform Rotation
    let xr = [];
    let yr = [];

    x.forEach(function(item, index){

        let new_x = ((x[index]-xc)*Math.cos(angle))-((y[index]-yc)*Math.sin(angle))+xc;
        let new_y = ((x[index]-xc)*Math.sin(angle))+((y[index]-yc)*Math.cos(angle))+yc;

        xr.push(new_x);
        yr.push(new_y);
    });

    // Write Rotation back to DOM
    $("."+shapestrg+"x").each(function(){
        $(this).val(xr[i]);
        i++;
    });

    i=0;

    $("."+shapestrg+"y").each(function(){
        $(this).val(yr[i]);
        i++;
    });

    areaAndCentroid(shapestrg);
};

function first_to_last(shapestrg){

    let x = $("#"+shapestrg+"firstX").val();
    let y = $("#"+shapestrg+"firstY").val();

    $("#"+shapestrg+"lastX").val(x);
    $("#"+shapestrg+"lastY").val(y);

    areaAndCentroid(shapestrg);

};

// Chart update

function UpdateChart(){

    let graphDiv = document.getElementById('SectionPlot')

    // wipe out the current traces
    while(graphDiv.data.length>0)
    {
        Plotly.deleteTraces(graphDiv, [0]);
    }

    //trace arrays
    let trace_shapes = [];
    // loop through the shapes and add section trace
    // and centroid
    for (let i=0; i<shape_count; i++){

        let shapestrg = "shape"+(i+1);
        let shapevoid = $('#'+shapestrg+'VoidSelect').val();
        let plotcolor = $('#'+shapestrg+'Color').val();

        let x = [];
        let y = [];
    
        //Get all X coordinates
        //Items are found in document order so X,Y pairs should be correct
        $("."+shapestrg+"x").each(function(){
            x.push(Number($(this).val()));
        });
    
        //Get all Y coordinates
        $("."+shapestrg+"y").each(function(){
            y.push(Number($(this).val()));
        });

        //Get Shape Centroid
        let xc = [Number($('#'+shapestrg+'Xc').html())];
        let yc = [Number($('#'+shapestrg+'Yc').html())];

        if (shapevoid == 0){
            trace_shapes.push({
                x: x,
                y: y,
                mode: 'lines+markers',
                name: shapestrg,
                fill: 'tozeroy',
                marker: {
                    size: 4,
                    color: plotcolor
                },
                line: {
                    color: plotcolor,
                    dash: 'dash',
                    width: 1
                },
            });

            trace_shapes.push({
                x: xc,
                y: yc,
                mode: 'markers',
                name: shapestrg+'_centroid',
                marker: {
                    size: 8,
                    color: plotcolor,
                    symbol: 'cross'
                },
            });

        } else {
            trace_shapes.push({
                x: x,
                y: y,
                mode: 'lines+markers',
                name: shapestrg,
                fill: 'tozeroy',
                marker: {
                    size: 4,
                    color: plotcolor
                },
                line: {
                    color: plotcolor
                },
            });

            trace_shapes.push({
                x: xc,
                y: yc,
                mode: 'markers',
                name: shapestrg+'_centroid',
                marker: {
                    size: 8,
                    color: plotcolor,
                    symbol: 'cross'
                },
            });
        }



    }

    if (modelRun == 1){
        trace_shapes.push({
            x: xx_axis_x,
            y: xx_axis_y,
            mode: 'lines+markers',
            name: "XX-Axis",
            marker: {
                size: 4,
                color: 'rgb(255, 0, 0)'
            },
            line: {
                color: 'rgb(255, 0, 0)',
                dash: 'dash'
            },
        });

        trace_shapes.push({
            x: yy_axis_x,
            y: yy_axis_y,
            mode: 'lines+markers',
            name: "YY-Axis",
            marker: {
                size: 4,
                color: 'rgb(0, 0, 255)'
            },
            line: {
                color: 'rgb(0, 0, 255)',
                dash: 'dash'
            },
        });

        trace_shapes.push({
            x: uu_axis_x,
            y: uu_axis_y,
            mode: 'lines+markers',
            name: "UU-Axis",
            marker: {
                size: 4,
                color: 'rgb(0, 255, 0)'
            },
            line: {
                color: 'rgb(0, 255, 0)',
                dash: 'dash'
            },
        });

        trace_shapes.push({
            x: vv_axis_x,
            y: vv_axis_y,
            mode: 'lines+markers',
            name: "VV-Axis",
            marker: {
                size: 4,
                color: 'rgb(255, 0, 255)'
            },
            line: {
                color: 'rgb(255, 0, 255)',
                dash: 'dash'
            },
        });

        trace_shapes.push({
            x: centroid_x,
            y: centroid_y,
            mode: 'markers',
            name: "Global Centroid",
            marker: {
                size: 10,
                color: 'rgb(0, 200, 0)',
                symbol: 'cross'
            },
        });
    }
    // Add Traces to Plot
    Plotly.addTraces(graphDiv, trace_shapes);
};

// This function is used for event handlers after the HTML document loads
function main() {

    // set units
    units = $('input[name="units"]:checked').val();

    // Initialize the chart
    let plot_type = 'lines+markers';
    let w = 420;
    let h = 700;

    let section_layout = {
        title: "Section Plot",
        width: w,
        height: h,
        showlegend: true,
        legend: {"orientation":"h"},
        margin: {
            l: 40,
            r: 40,
            b: 50,
            t: 80,
            pad: 4
          },
        yaxis: {
            scaleanchor: "x",
        }
    };

    var trace1 = {
        x: [0,1,1,0],
        y: [0,0,1,0],
        mode: plot_type,
        name: 'shape1',
        marker: {
            size: 4,
            color: 'rgb(180, 0, 0)'
        },
        line: {
            color: 'rgb(150, 0, 0)'
        },
    };

    var trace2 = {
        x: [0.5],
        y: [0.25],
        mode: 'markers',
        name: 'shape1_centroid',
        marker: {
            size: 4,
            color: 'rgb(150, 0, 0)',
            symbol: 'cross'
        },
    };

    Plotly.newPlot("SectionPlot", [trace1,trace2], section_layout);
    
    for(let i=0; i<shape_count; i++){

        let shapestrg = "shape"+(i+1);
        areaAndCentroid(shapestrg);
    };
    
        // Units toggle
    $('input:radio[name="units"]').change(function() {
        
        modelRun = 0;

        units = $(this).val();

        if(units == "imperial"){
            // remove all btn- classes to avoid duplicates
            $("#metric_button").removeClass("btn-secondary");
            $("#metric_button").removeClass("btn-primary");
            $("#imperial_button").removeClass("btn-primary");
            $("#imperial_button").removeClass("btn-secondary");
            
            $("#imperial_button").addClass("btn-primary");
            $("#metric_button").addClass("btn-secondary");
            
            // change all stress units
            $('.stress_units').each(function(){
                $(this).html("ksi");
            });

            // change all lengths
            $('.length_units').each(function() {
                $(this).html("in");
            });
            
            // change all Areas
            $('.area_units').each(function() {
                $(this).html("in<sup>2</sup>");
            });

            // change all x vertex header
            $('.xvertexheader').each(function() {
                $(this).html("X(in)");
            });

            // change all y vertex header
            $('.yvertexheader').each(function() {
                $(this).html("Y(in)");
            });
            

        } else {
            // remove all btn- classes to avoid duplicates
            $("#metric_button").removeClass("btn-secondary");
            $("#metric_button").removeClass("btn-primary");
            $("#imperial_button").removeClass("btn-primary");
            $("#imperial_button").removeClass("btn-secondary");
            
            $("#metric_button").addClass("btn-primary");
            $("#imperial_button").addClass("btn-secondary");
            
            // change all stress units
            $('.stress_units').each(function(){
                $(this).html("MPa");
            });

            // change all lengths
            $('.length_units').each(function() {
                $(this).html("mm")
            });

            // change all Areas
            $('.area_units').each(function() {
                $(this).html("mm<sup>2</sup>");
            });

            // change all x vertex header
            $('.xvertexheader').each(function() {
                $(this).html("X(mm)");
            });

            // change all y vertex header
            $('.yvertexheader').each(function() {
                $(this).html("Y(mm)");
            });
            
        }
    });


    $("#accordion").on("change",function(){
        UpdateChart();
    });
    
    $("#add_shape").click(function(){

        shape_count += 1;
        $("#numshapes").val(shape_count);
        let shapestrg = "shape"+shape_count;
        let new_card = newshapecard(shapestrg);
        
        $("#accordion").append(new_card);
        modelRun = 0;

        areaAndCentroid(shapestrg);

    });

    $("#remove_shape").click(function(){

        if(shape_count > 1){
            let shapestrg = 'shape'+ shape_count;

            $("#"+shapestrg+"Card").remove();

            shape_count -= 1;
            $("#numshapes").val(shape_count);
            modelRun = 0;

        }

        UpdateChart();

    });


};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
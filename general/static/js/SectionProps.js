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

// This function is used for event handlers after the HTML document loads
function main() {
    // Initialize the chart
    var ctx = document.getElementById("sectionCanvas").getContext("2d");
        
    var sectionChart = new Chart(ctx,{
        type: 'scatter',
        data:{
            datasets:[{
                label: "Section",
                data: [{x:0,y:0}],
                backgroundColor: 'rgb(255,0,0)',
                showLine: true,
                fill: {target: 'shape', above: 'rgba(255,0,0,0.2)', below:'rgba(255,0,0,0.2)'},
                // borderDash: [10,5],
            },
            {
                label: "Centroid",
                data: [{x:0,y:0}],
                backgroundColor: 'rgb(0,0,255)',
            },
            {
                label: "xx",
                data: [{x:0,y:0}],
                backgroundColor: 'rgba(0,255,0,0.7)',
                showLine: true,
                borderColor: 'rgba(0,255,0,0.7)',
                borderDash: [10,5]
            },
            {
                label: "yy",
                data: [{x:0,y:0}],
                backgroundColor: 'rgba(255,0,0,0.7)',
                showLine: true,
                borderColor: 'rgba(255,0,0,0.7)',
                borderDash: [10,5]
            },
            {
                label: "uu",
                data: [{x:0,y:0}],
                backgroundColor: 'rgba(255,51,255,0.3)',
                showLine: true,
                borderColor: 'rgba(255,51,255,0.3)',
                borderDash: [10,5,5,5]
            },
            {
                label: "vv",
                data: [{x:0,y:0}],
                backgroundColor: 'rgba(51,255,255,0.3)',
                showLine: true,
                borderColor: 'rgba(51,255,255,0.3)',
                borderDash: [10,5,5,5]
            }]
        }

    });
    
    UpdateChart();
    
    // Add a new data entry row for a new vertex
    $("#addVertex, #addBelowFirst").on("click", function(){
        
        $("#vertexTable tbody tr:last").before(
        '<tr class=\"user vertex\">' +
        '<td>' + Number($("#vertexTable tbody tr").length).toString() + '</td>' +
        '<td><input name=\"x\" class=\"x input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\"></td>' +
        '<td><input name=\"y\" class=\"y input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\"></td>' +
        '<td>' +
        '<button type=\"button\" class=\"addBelow btn btn-secondary btn-success btn-sm\">' +
        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
        '</svg>' + 
        '</button>' +
        '<a href=\"#\" class=\"removeButton badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
        '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
        '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
        '</svg></a></td>' +
        '</tr>'
        );
    });
    
    // Change the last x value to match the first x value
    $("#firstX").change(function(){
        $("#lastX").val($(this).val());
        UpdateChart();
    });
    
    // Change the last y value to match the first y value
    $("#firstY").change(function(){
        $("#lastY").val($(this).val());
        UpdateChart();
    });
    
    // Removing row that was clicked
    $("tbody").on("click", ".removeButton", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //remove the row
        $(this).closest("tr").remove();
        
        //expand function to renumber the remaining vertices
        tableBody.children('.user').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text(String(i+1));
        });
        
        UpdateChart();
        
    });
    
    // Add row Above that was clicked
    $("tbody").on("click", ".addAbove", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        $newRow = $curRow.clone(true)
        
        $curRow.before($newRow)
        
        //expand function to renumber the remaining vertices
        tableBody.children('.user').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text(String(i+1));
        });
        
        UpdateChart();
        
    });
    
    // Add row Below that was clicked
    $("tbody").on("click", ".addBelow", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        $newRow = $curRow.clone(true)
        
        $curRow.after($newRow)
        
        //expand function to renumber the remaining vertices
        tableBody.children('.user').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text(String(i+1));
        });
        
        UpdateChart();
        
    });
    
    $("#vertexTable").on("change",function(){
        UpdateChart();
    });
    
    function UpdateChart(){
        
        //Get the x,y coordinates from the vertices table
        var data = [];
        var xcoor = [];
        var ycoor = [];
        $(".vertex").each(function(){
            var xs = $(this).find(".x").val();
            var ys = $(this).find(".y").val();
            
            data.push({x: Number(xs),y: Number(ys)});
            xcoor.push(xs);
            ycoor.push(ys);
        });
        
        //console.log(data);
        //console.log(sectionChart.data.datasets[0].data);
        //console.log(xcoor);
        //console.log(ycoor);
        
        // Get min and max x,y points to
        // set the scale for the x,y axis
        // to get a better aspect ratio on the
        // plotted section
        minx = Math.min(...xcoor);
        maxx = Math.max(...xcoor);
        miny = Math.min(...ycoor);
        maxy = Math.max(...ycoor);
        
        //console.log(minx);
        //console.log(maxx);
        //console.log(miny);
        //console.log(maxy);
        
        // Bounding box -- cheaper than actual centroid
        var y_span = maxy-miny;
        var x_span = maxx-minx;
        
        var mid_x = maxx- (x_span/2.0);
        var mid_y = maxy - (y_span/2.0);
        
        var span = Math.max(y_span,x_span)+2;
        
        // x and y axis ranges starting from the bounding
        // box center.
        
        var chart_x_min = mid_x - (span/2.0);
        var chart_x_max = mid_x + (span/2.0);
        var chart_y_min = mid_y - (span/2.0);
        var chart_y_max = mid_y + (span/2.0);
        
        //console.log([chart_x_max,chart_x_min,chart_y_max,chart_y_min]);
        
        var scale_pts = [{x: chart_x_min,y: chart_y_min},{x: chart_x_max,y: chart_y_max}];
        
        sectionChart.data.datasets[0].data = data;
        // sectionChart.data.datasets[2].data = scale_pts;
        
        // Set Chart.js axis scales
        sectionChart.options.scales = {
            x: {
                display: true,
                min: chart_x_min,
                max: chart_x_max
            },
            y: {
                display: true,
                min: chart_y_min,
                max: chart_y_max
            }
        };
        
        sectionChart.update();
        
        UpdateCentroid();
        
    };
    
    function UpdateCentroid(){
        sectionChart.data.datasets[1].data = centroid;
        sectionChart.data.datasets[2].data = xx_axis;
        sectionChart.data.datasets[3].data = yy_axis;
        sectionChart.data.datasets[4].data = uu_axis;
        sectionChart.data.datasets[5].data = vv_axis;
        sectionChart.update();
    };
};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
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
    var ctx = document.getElementById("weldCanvas").getContext("2d");
        
    var weldChart = 0;
    
    UpdateChart();
        
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
    
    // Add row Below that was clicked
    $("tbody").on("click", ".addWeldFirst", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        $newRow =   '<tr class=\"user segment\">' +
                    '<td class=\"suid\">' + Number($("#vertexTable tbody tr").length).toString() + '</td>' +
                    '<td><input name=\"xi\" class=\"xi input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\"></td>' +
                    '<td><input name=\"yi\" class=\"yi input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\"></td>' +
                    '<td><input name=\"xj\" class=\"xj input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\"></td>' +
                    '<td><input name=\"yj\" class=\"yj input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\"></td>' +
                    '<td>' +
                    '<button type=\"button\" class=\"addWeld btn btn-secondary btn-success btn-sm\">' +
                    '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                    '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                    '</svg>' + 
                    '</button>' +
                    '<a href=\"#\" class=\"removeButton badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
                    '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
                    '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
                    '</svg></a></td>' +
                    '</tr>'
        
        $curRow.after($newRow)
        
        //expand function to renumber the remaining vertices
        tableBody.children('.user').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text(String(i+1));
        });
        
        UpdateChart();
        
    });

    // Add a copy of the row Below that was clicked
    $("tbody").on("click", ".addWeld", function(){
        
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
    
    $("#weldTable").on("change",function(){
        UpdateChart();
    });
    
    $("#userLoadPoint").on("change",function(){
        UpdateChart();
    });
    
    $("#user_x").on("change",function(){
        UpdateChart();
    });
    
    $("#user_y").on("change",function(){
        UpdateChart();
    });
    
    function UpdateChart(){
        
        if (weldChart !==0){
            weldChart.destroy();
        };
        
        weldChart = new Chart(ctx,{
        type: 'scatter',
        data:{
            datasets:[{
                label: 's1',
                data: [{x:0,y:0}],
                backgroundColor: 'rgb(255,0,0)',
                fill: {target: 'shape', above: 'rgba(255,0,0,0.2)', below:'rgba(255,0,0,0.2)'},
                showLine: true,
                borderColor: 'rgb(0,0,0)'
            }
            ]
        }

        });
        
        weldChart.update();

        var xcoord = []
        var ycoord = []
        
        $(".segment").each(function(){
            var data = []
            var xi = $(this).find(".xi").val();
            var yi = $(this).find(".yi").val();
            var xj = $(this).find(".xj").val();
            var yj = $(this).find(".yj").val();
            var suid = $(this).find(".suid").text();
            
            data.push({x: Number(xi),y: Number(yi)},
                {x: Number(xj),y: Number(yj)});
            
            if(suid === "1"){
                weldChart.data.datasets[0].data = data;
            } else {
                weldChart.data.datasets.push({
                    label: 's'+Number(suid).toString(),
                    data: data,
                    backgroundColor: 'rgb(255,0,0)',
                    fill: {target: 'shape', above: 'rgba(0,0,0,1)', below:'rgba(0,0,0,1)'},
                    showLine: true,
                    borderColor: 'rgb(0,0,0)'
                });
                
            };
            
            xcoord.push(xi);
            ycoord.push(yi);
            xcoord.push(xj);
            ycoord.push(yj);
        });
        
        // Check if the load point is by the user
        // if so include the load point in the max/min
        // comptutations for chart scaling
        
        var user_load_location = $('select[name="loadPosition"]').val();
        var user_x = $('.user_x').val();
        var user_y = $('.user_y').val();
        
        if(user_load_location ==='user'){
            xcoord.push(user_x);
            ycoord.push(user_y);
            
            weldChart.data.datasets.push({
                    label: 'User_load',
                    data: [{x: user_x,y: user_y}],
                    backgroundColor: 'rgb(0,255,0)',
                    fill: {target: 'shape', above: 'rgba(0,0,0,1)', below:'rgba(0,0,0,1)'},
                    showLine: true,
                    borderColor: 'rgb(0,255,0)'
                });
        } else {
            
            
        };
        
        // check the centroid variable is not 0
        // and if not plot the centroid point
        console.log(centroid);
        console.log(centroid!==[0]);
        
        if(centroid!==[0]){
            weldChart.data.datasets.push({
                label: 'Centroid',
                data: centroid,
                backgroundColor: 'rgb(0,0,255)',
                fill: {target: 'shape', above: 'rgba(0,0,0,1)', below:'rgba(0,0,0,1)'},
                showLine: true,
                borderColor: 'rgb(0,0,255)'
            });
        };
        
        // Get min and max x,y points to
        // set the scale for the x,y axis
        // to get a better aspect ratio on the
        // plotted section
        minx = Math.min(...xcoord);
        maxx = Math.max(...xcoord);
        miny = Math.min(...ycoord);
        maxy = Math.max(...ycoord);
        
        // Bounding box -- cheaper than actual centroid
        var y_span = maxy-miny;
        var x_span = maxx-minx;
        
        var mid_x = maxx- (x_span/2.0);
        var mid_y = maxy - (y_span/2.0);
        
        var span = Math.max(y_span,x_span)+0.5;
        
        // x and y axis ranges starting from the bounding
        // box center.
        
        var chart_x_min = mid_x - (span/2.0);
        var chart_x_max = mid_x + (span/2.0);
        var chart_y_min = mid_y - (span/2.0);
        var chart_y_max = mid_y + (span/2.0);
        
        // Set Chart.js axis scales
        weldChart.options.scales.xAxes[0].ticks = {
                min: chart_x_min,
                max: chart_x_max,
                stepSize: x_span/10.0
            };
            
        weldChart.options.scales.yAxes[0].ticks = {
                min: chart_y_min,
                max: chart_y_max,
                stepSize: y_span/10.0
            };

        weldChart.update();

    };
    
};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
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

    // Initialize the linear chart
    var ctx = document.getElementById("linearCanvas").getContext("2d");
    
    var linearChart = 0;

    updateLinearChart();

    // Initialize the bilinear chart
    var bilin_base = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [0,1,1,0,0],
        y: [0,0,1,1,0],
        z: [0,0,0,0,0],
        opacity: 1,
        line: {
            width: 2,
            color: 'rgb(0,0,0)',
            dash: 'dash',
        },
        marker: {
            size: 3,
            color: 'rgb(255,0,0)',
        }

    };

    var bilin_x1y1 = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [0,0],
        y: [0,0],
        z: [0,1],
        opacity: 1,
        line: {
            width: 2,
            color: 'rgb(0,0,0)',
            dash: 'dashdot',
        },
        marker: {
            size: 3,
            color: 'rgb(255,0,0)',
        }
    };

    var bilin_x1y2 = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [0,0],
        y: [1,1],
        z: [0,0.5],
        opacity: 1,
        line: {
            width: 2,
            color: 'rgb(0,0,0)',
            dash: 'dashdot',
        },
        marker: {
            size: 3,
            color: 'rgb(255,0,0)',
        }
    };

    var bilin_x2y1 = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [1,1],
        y: [0,0],
        z: [0,1],
        opacity: 1,
        line: {
            width: 2,
            color: 'rgb(0,0,0)',
            dash: 'dashdot',
        },
        marker: {
            size: 3,
            color: 'rgb(255,0,0)',
        }
    };

    var bilin_x2y2 = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [1,1],
        y: [1,1],
        z: [0,0.5],
        opacity: 1,
        line: {
            width: 2,
            color: 'rgb(0,0,0)',
            dash: 'dashdot',
        },
        marker: {
            size: 3,
            color: 'rgb(255,0,0)',
        }
    };

    var bilin_top = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [0,1,1,0,0],
        y: [0,0,1,1,0],
        z: [1,1,0.5,0.5,1],
        opacity: 1,
        line: {
            width: 2,
            color: 'rgba(0,0,255,0.5)',
        },
        marker: {
            size: 3,
            color: 'rgb(255,0,0)',
        }
    };

    var bilin_xy = {
        type: 'scatter3d',
        mode: 'lines',
        x: [0.5,0.5],
        y: [0.5,0.5],
        z: [0,0.75],
        opacity: 1,
        line: {
            width: 4,
            color: 'rgb(0,0,0)',
            dash: 'dashdot',
        },
    };

    var bilin_res = {
        type: 'scatter3d',
        mode: 'markers',
        x: [0.5],
        y: [0.5],
        z: [0],
        opacity: 1,
        marker: {
            width: 4,
            color: 'rgb(0,0,255)',
        },
    };

    var bilin_midline_x = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [0.5,0.5,0.5,0.5],
        y: [0,0,1,1],
        z: [0,1,0.5,0],
        opacity: 1,
        line: {
            width: 3,
            color: 'rgb(0,255,0)',
            dash: 'dash',
        },
        marker: {
            size: 3,
            color: 'rgb(0,255,0)',
        }
    };

    var bilin_midline_y = {
        type: 'scatter3d',
        mode: 'lines+markers',
        x: [0,0,1,1],
        y: [0.5,0.5,0.5,0.5],
        z: [0,0.75,0.75,0],
        opacity: 1,
        line: {
            width: 3,
            color: 'rgb(0,255,0)',
            dash: 'dash',
        },
        marker: {
            size: 3,
            color: 'rgb(0,255,0)',
        }
    };

    var bilin_plot_data = [bilin_base, bilin_x1y1, bilin_x1y2, bilin_x2y1, bilin_x2y2,bilin_top,bilin_midline_x,bilin_midline_y,bilin_xy,bilin_res];

    var plot_layout = {
        height: 400,
        width: 400,
        margin: {
            l: 10,
            r: 10,
            b: 5,
            t: 10,
            pad: 4
          },
        showlegend: false,
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        scene: {
            xaxis: {
                backgroundcolor:"rgb(216,216,225)",
                gridcolor:"white",
                showbackground:true,
                zerolinecolor:"white",},
            yaxis: {
                backgroundcolor:"rgb(216,216,225)",
                gridcolor:"white",
                showbackground:true,
                zerolinecolor:"white"},
            zaxis: {
                backgroundcolor:"rgb(216,216,225)",
                gridcolor:"white",
                showbackground:true,
                zerolinecolor:"white",},
        },

    }

    Plotly.newPlot('bilinearChart',bilin_plot_data,plot_layout);

    $("#btn_calc_linear").click(function(){

        let x1 = Number($('#x1').val());
        let x = Number($('#x').val());
        let x2 = Number($('#x2').val());
        let y1 = Number($('#y1').val());
        let y2 = Number($('#y2').val());

        let y = linear_interpolate(x1,y1,x2,y2,x);

        if(y[1]==1){
            $('#y').html(y[0].toFixed(4).toString());
            $('#y').addClass("table-success");
            $('#y').removeClass("table-danger");
            $('#y').removeClass("table-warning");

            updateLinearChart();

        } else {
            $('#y').html(y[0]);
            $('#y').addClass("table-danger");
            $('#y').removeClass("table-success");
            $('#y').removeClass("table-warning");

            updateLinearChart();
        };
        
    });

    $(".linearuser").on("change",function(){
        $('#y').html('--');
        $('#y').addClass("table-warning");
        $('#y').removeClass("table-success");
        $('#y').removeClass("table-danger");
    });

    function updateLinearChart(){
        if (linearChart !==0){
            linearChart.destroy();
        };
        
        let yp = $('#y').html();

        if(yp==="x must be between x1 and x2"){
            yp=0;
        } else {
            yp = Number(yp);
        }

        linearChart = new Chart(ctx,{
        type: 'scatter',
        width: 200,
        data:{
            datasets:[{
                label: 'P1',
                data: [{x:Number($('#x1').val()),y:0},{x:Number($('#x1').val()),y:Number($('#y1').val())}],
                backgroundColor: 'rgb(255,0,0)',
                showLine: true,
                borderColor: 'rgb(0,0,0)',
                borderDash: [10,15],
                borderWidth:1,
            },
            {
                label: 'P2',
                data: [{x:Number($('#x2').val()),y:0},{x:Number($('#x2').val()),y:Number($('#y2').val())}],
                backgroundColor: 'rgb(255,0,0)',
                showLine: true,
                borderColor: 'rgb(0,0,0)',
                borderDash: [10,15],
                borderWidth:1,
            },
            {
                label: 'P',
                data: [{x:Number($('#x').val()),y:0},{x:Number($('#x').val()),y:yp}],
                backgroundColor: 'rgb(0,0,255)',
                showLine: true,
                borderColor: 'rgb(0,0,0)',
                borderDash: [20,5,8,5],
                borderWidth:1,
            },
            {
                label: 'Line',
                data: [{x:Number($('#x1').val()),y:Number($('#y1').val())},{x:Number($('#x2').val()),y:Number($('#y2').val())}],
                backgroundColor: 'rgba(255,0,0,0.1)',
                fill: 'origin',
                showLine: true,
                borderColor: 'rgb(0,0,0)',
                borderWidth:1,
            },
            ]
        },
        options:{
            responsive: true,
            maintainAspectRatio: false,
            legend: {display: false},
        },

        });
        
        linearChart.update();
    };

    $("#btn_calc_bilinear").click(function(){

        let x1 = Number($('#bx1').val());
        let x = Number($('#bx').val());
        let x2 = Number($('#bx2').val());
        let y1 = Number($('#by1').val());
        let y = Number($('#by').val());
        let y2 = Number($('#by2').val());
        let f11 = Number($('#bx1y1').val());
        let f12 = Number($('#bx1y2').val());
        let f21 = Number($('#bx2y1').val());
        let f22 = Number($('#bx2y2').val());

        let res = bilinear_interpolate(x1,y1,x2,y2,x,y,f11,f12,f21,f22);

        let status = res[2];
        let fxy = res[0];
        let fx1y = res[1][0];
        let fx2y = res[1][1];
        let fxy1 = res[1][2];
        let fxy2 = res[1][3];

        
        $('#bx1y').html(fx1y.toFixed(4).toString());
        $('#bx2y').html(fx2y.toFixed(4).toString());
        $('#bxy1').html(fxy1.toFixed(4).toString());
        $('#bxy2').html(fxy2.toFixed(4).toString());

        if(status==1){
            $('#bxy').html(fxy.toFixed(4).toString());

            $('.bilinres').each(function(){
                $(this).addClass("table-success");
                $(this).removeClass("table-danger");
                $(this).removeClass("table-warning");
            });

            //update the plotly chart
            //bilin_plot_data = [bilin_base, bilin_x1y1, bilin_x1y2, bilin_x2y1, bilin_x2y2,bilin_top,bilin_midline_x,bilin_midline_y,bilin_xy]

            //base
            bilin_plot_data[0]['x'] = [x1,x2,x2,x1,x1];
            bilin_plot_data[0]['y'] = [y1,y1,y2,y2,y1];

            //f(x1,y1)
            bilin_plot_data[1]['x'] = [x1,x1];
            bilin_plot_data[1]['y'] = [y1,y1];
            bilin_plot_data[1]['z'] = [0,f11];

            //f(x1,y2)
            bilin_plot_data[2]['x'] = [x1,x1];
            bilin_plot_data[2]['y'] = [y2,y2];
            bilin_plot_data[2]['z'] = [0,f12];

            //f(x2,y1)
            bilin_plot_data[3]['x'] = [x2,x2];
            bilin_plot_data[3]['y'] = [y1,y1];
            bilin_plot_data[3]['z'] = [0,f21];

            //f(x2,y2)
            bilin_plot_data[4]['x'] = [x2,x2];
            bilin_plot_data[4]['y'] = [y2,y2];
            bilin_plot_data[4]['z'] = [0,f22];

            //top
            bilin_plot_data[5]['x'] = [x1,x2,x2,x1,x1];
            bilin_plot_data[5]['y'] = [y1,y1,y2,y2,y1];
            bilin_plot_data[5]['z'] = [f11,f21,f22,f12,f11];

            //midline x
            bilin_plot_data[6]['x'] = [x,x,x,x];
            bilin_plot_data[6]['y'] = [y1,y1,y2,y2];
            bilin_plot_data[6]['z'] = [0,fxy1,fxy2,0];

            //midline y
            bilin_plot_data[7]['x'] = [x1,x1,x2,x2];
            bilin_plot_data[7]['y'] = [y,y,y,y];
            bilin_plot_data[7]['z'] = [0,fx1y,fx2y,0];

            //result
            bilin_plot_data[8]['x'] = [x,x];
            bilin_plot_data[8]['y'] = [y,y];
            bilin_plot_data[8]['z'] = [0,fxy];

            bilin_plot_data[9]['x'] = [x];
            bilin_plot_data[9]['y'] = [y];
            bilin_plot_data[9]['z'] = [fxy];

            //set axis ranges
/*             x_max = Math.max(x1,x2,x) + 0.5;
            x_min = Math.min(x1,x2,x) - 0.5;
            y_max = Math.max(y1,y2,y) + 0.5;
            y_min = Math.min(y1,y2,y) - 0.5;
            z_max = Math.max(f11,f12,f21,f22) + 0.5;
            z_min = Math.min(f11,f12,f21,f22) - 0.5;
  

            plot_layout['scene']['yaxis']['range']=[y_min,y_max];
            plot_layout['scene']['xaxis']['range']=[x_min,x_max];
            plot_layout['scene']['zaxis']['range']=[z_min,z_max]; */

            //redraw the chart
            Plotly.redraw('bilinearChart');

        } else {
            $('#bxy').html(fxy);

            $('.bilinres').each(function(){
                $(this).addClass("table-danger");
                $(this).removeClass("table-success");
                $(this).removeClass("table-warning");
            });

        };
        
    });

    $(".bilinearuser").on("change",function(){
        $('.bilinres').each(function(){
            $(this).html(0)
            $(this).addClass("table-warning");
            $(this).removeClass("table-success");
            $(this).removeClass("table-danger");
        });
    });

};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
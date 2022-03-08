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

function updateChart(){

    // Get the canvas element size
    var canvas = document.getElementById("fndCanvas");
    var canvas_x = canvas.width;
    var canvas_y = canvas.height;
    var ctx = canvas.getContext("2d");

    // Clear the Canvas
    ctx.clearRect(0,0,canvas_x, canvas_y);

    // Get the force application elevation
    let h = Number($('#h').val());

    // Check if the dtotal element exists
    // will only exist if the calc has been run.
    let d_exist = !!document.getElementById("dtotal");

    // initialize d so the plot can update before results exist.
    let d = 10;
    console.log(d_exist);

    // if #dtotal exists calc has been run so grab that value
    // to replace the initialized value of d.
    if(d_exist){
        d = Number($('#dtotal').html());
    }
    
    // Assume the load application height of pier embedment will always be
    // the controlling dimensions. Canvas is hard coded to be 800 pxs tall
    // allow for a 20 px margin which leaves 380 px to mid height.
    let sf = 380/Math.max(h,d);

    // get the size of the pier
    let b =  Number($('#shape_size').val());

    // get the ignore depth
    let d_ignore = Number($('#d_ignore').val());

    // plot soil
    let x1 = 10;
    let x2 = 390;
    let y1 = 400;
    let y2 = 400+(sf*d)+8;

    ctx.fillStyle = "rgba(179,89,0,0.8)";
    ctx.beginPath();
    ctx.lineWidth=1;
    ctx.moveTo(x1,y1);
    ctx.lineTo(x1,y2);
    ctx.lineTo(x2,y2);
    ctx.lineTo(x2,y1);
    ctx.lineTo(x1,y1);
    ctx.stroke();
    ctx.fill();

    ctx.fillStyle = "rgb(0,0,0)";

    // plot the ignore depth
    x1 = 10;
    x2 = 390;
    y1 = 400;
    y2 = 400+(sf*d_ignore);

    ctx.fillStyle = "rgba(255,0,0,0.5)";
    ctx.beginPath();
    ctx.lineWidth=1;
    ctx.moveTo(x1,y1);
    ctx.lineTo(x1,y2);
    ctx.lineTo(x2,y2);
    ctx.lineTo(x2,y1);
    ctx.lineTo(x1,y1);
    ctx.stroke();
    ctx.fill();

    ctx.fillStyle = "rgb(0,0,0)";

    // plot the grass line
    ctx.strokeStyle = "rgb(0,255,0)";
    ctx.beginPath();
    ctx.lineWidth=4;
    ctx.moveTo(10,400);
    ctx.lineTo(390,400);
    ctx.stroke();

    ctx.strokeStyle = "rgb(0,0,0)";

    // Label Ignore Depth
    // label after the ground is drawn so the dim line is at a higher z index

    ctx.font = 'bold 14px monospace';
    ctx.textAlign = "center";
    let label = d_ignore.toFixed(3).toString()+" ft";

    if(d_ignore > 0){

      let w = ctx.measureText(label).width;

      ctx.beginPath();
      ctx.lineWidth=1;
      ctx.moveTo(100,y2)
      ctx.lineTo(100,(y1-(w+20)));
      ctx.stroke();

      // Tick Marks
      ctx.beginPath();
      ctx.moveTo(95,y2-5);
      ctx.lineTo(105,y2+5);
      ctx.stroke();

      // Tick Marks
      ctx.beginPath();
      ctx.moveTo(95,y1-5);
      ctx.lineTo(105,y1+5);
      ctx.stroke();

      // Vertical text
      // save current context
      ctx.save();
      ctx.translate(98,(y1-w));
      ctx.rotate(-Math.PI/2);

      ctx.fillText(label, (-w/2)+10, -2);

      // restore the original context
      ctx.restore();

    }

    // plot pier
    x1 = 200 - (sf*(b/24));
    x2 = x1 + (sf*(b/12));
    y1 = 400;
    y2 = y1 + (sf*d);

    ctx.fillStyle = "rgb(204,204,204)";
    ctx.beginPath();
    ctx.lineWidth=1;
    ctx.moveTo(x1,y1);
    ctx.lineTo(x1,y2);
    ctx.lineTo(x2,y2);
    ctx.lineTo(x2,y1);
    ctx.lineTo(x1,y1);
    ctx.stroke();
    ctx.fill();

    ctx.fillStyle = "rgb(0,0,0)";

    // label the pier depth below d,ignore
    label = (d-d_ignore).toFixed(3).toString()+" ft";

    // dim vert line
    ctx.beginPath();
    ctx.moveTo(100,(400+(sf*d_ignore)));
    ctx.lineTo(100,y2);
    ctx.stroke();

    // dim ext line to pier
    ctx.beginPath();
    ctx.moveTo(95,y2);
    ctx.lineTo(x1-4,y2);
    ctx.stroke();

    // Tick Marks
    ctx.beginPath();
    ctx.moveTo(95,(400+(sf*d_ignore))-5);
    ctx.lineTo(105,(400+(sf*d_ignore))+5);
    ctx.stroke();

    // Tick Marks
    ctx.beginPath();
    ctx.moveTo(95,y2-5);
    ctx.lineTo(105,y2+5);
    ctx.stroke();

    // Vertical text
    // save current context
    ctx.save();
    ctx.translate(98,(y2-(0.5*sf*(d-d_ignore))));
    ctx.rotate(-Math.PI/2);

    ctx.fillText(label, 0, -2);

    // restore the original context
    ctx.restore();

    // label the pier depth below ground
    label = d.toFixed(3).toString()+" ft";

    // dim vert line
    ctx.beginPath();
    ctx.moveTo(300,400);
    ctx.lineTo(300,y2);
    ctx.stroke();

    // dim ext line to pier
    ctx.beginPath();
    ctx.moveTo(305,y2);
    ctx.lineTo(x2+4,y2);
    ctx.stroke();

    // Tick Marks
    ctx.beginPath();
    ctx.moveTo(295,395);
    ctx.lineTo(305,405);
    ctx.stroke();

    // Tick Marks
    ctx.beginPath();
    ctx.moveTo(295,y2-5);
    ctx.lineTo(305,y2+5);
    ctx.stroke();

    // Vertical text
    // save current context
    ctx.save();
    ctx.translate(298,(y2-(0.5*sf*d)));
    ctx.rotate(-Math.PI/2);

    ctx.fillText(label, 0, -2);

    // restore the original context
    ctx.restore();

    // plot the load point
    x1 = 200;
    x2 = 300;
    y1 = 400 - (sf*h);

    ctx.beginPath();
    ctx.lineWidth=2;
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y1);
    ctx.stroke();

    // arrow head
    ctx.beginPath();
    ctx.lineWidth=2;
    ctx.moveTo(x1+5,y1-5);
    ctx.lineTo(x1,y1);
    ctx.lineTo(x1+5,y1+5);
    ctx.stroke();

    label = "P:"+$('#p').val()+" lbs";
    w = ctx.measureText(label).width;
    ctx.fillText(label, 250, y1-6);

    // label the load application point height
    label = h.toFixed(3).toString()+" ft";
    ctx.lineWidth=1;
    // dim vert line
    ctx.beginPath();
    ctx.moveTo(300,400);
    ctx.lineTo(300,y1);
    ctx.stroke();

    // Tick Marks
    ctx.beginPath();
    ctx.moveTo(295,395);
    ctx.lineTo(305,405);
    ctx.stroke();

    // Tick Marks
    ctx.beginPath();
    ctx.moveTo(295,y1-5);
    ctx.lineTo(305,y1+5);
    ctx.stroke();

    // Vertical text
    // save current context
    ctx.save();
    ctx.translate(298,(y1+(0.5*sf*h)));
    ctx.rotate(-Math.PI/2);

    ctx.fillText(label, 0, -2);

    // restore the original context
    ctx.restore();

};

function main() {

    updateChart();

    $('.chart_input').change(function() {
        updateChart();

          // Get the canvas element size
        var canvas = document.getElementById("fndCanvas");
        var ctx = canvas.getContext("2d");
        ctx.font = 'bold 24px monospace';
        ctx.fillText("** NOT CURRENT **", 200, 50);
    });

};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
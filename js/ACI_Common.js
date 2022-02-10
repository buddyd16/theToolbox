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

var ACI_Bars = {
    3: [0.375,0.11,0.376],
    4: [0.500,0.20,0.668],
    5: [0.625,0.31,1.043],
    6: [0.750,0.44,1.502],
    7: [0.875,0.60,2.044],
    8: [1.000,0.79,2.670],
    9: [1.128,1.00,3.400],
    10: [1.270,1.27,4.303],
    11: [1.410,1.56,5.313],
    14: [1.693,2.25,7.65],
    18: [2.257,4.00,13.60],
};

function ACI_Beta1(fc_psi){
    
    if (fc_psi<= 4000){
        return 0.85;
    } else if (fc_psi <= 8000){
        return (0.85 - ((0.05*(fc_psi-4000))/1000));
    } else {
        return 0.65;
    }
};

function PerpOfLine(x1,y1,x2,y2){

    var x = x2-x1;
    var y = y2-y1;
    const len = Math.sqrt(x*x + y*y);
    var ux = x/len;
    var uy = y/len;
    return [-uy,ux];
};

function yAtX(x1,y1,x2,y2,x3){
    // parametric function for x to solve for t
    // x(t) = x1 + t*(x2-x1)
    // x3 - x1 / (x2-x1) = t
    var t = (x3-x1)/(x2-x1);

    return y1 + t*(y2-y1);
};

function xAtY(x1,y1,x2,y2,y3){
    // parametric function for x to solve for t
    // x(t) = x1 + t*(x2-x1)
    // x3 - x1 / (x2-x1) = t
    var t = (y3-y1)/(y2-y1);

    return x1 + t*(x2-x1);
};

function ACI_Standard_Bar_Radius(bar){

    var db = bar[0];

    if (db<=1.000){
        return [6*db,(6*db)+db,(6*db)+(db/2)];
    } else if(db<=1.410){
        return [8*db,(8*db)+db,(8*db)+(db/2)];
    } else {
        return [10*db,(10*db)+db,(10*db)+(db/2)];
    }
}
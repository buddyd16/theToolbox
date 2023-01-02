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

function nds_actual_dimensions(b_nom,d_nom,num_plys){
    /*
    b_nom = String of nominal width
    d_nom = String of nominal depth

    returns an array [b,d]

    b_nom is assumed to be the narrow edge
    d_nom is assumed to be the long edge
    */

    let b; 
    let d;

    if (Number(b_nom)> 6){
        b = Number(b_nom) - 0.75;
    } else {
        b = Number(b_nom) - 0.5;
    };

    if (Number(d_nom)>6){
        d = Number(d_nom) - 0.75;
    } else{
        d = Number(d_nom) - 0.5;
    };

    // Account for Number of Plys, assuming narrow side is the built up dimension.
    b = b*num_plys;

    return [b,d];

};
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

//Function to Compute Ld
function compute_Ld(){
    var db = Number($('#tbl_db').html());
    var lambda = Number($('#aci_lambda').val());
    var fpc_psi = Number($('#fpc_psi').val());
    var fy_psi = Number($('#fy_psi').val());
    var aci_psi_t = Number($('#aci_psi_t').val());
    var aci_psi_e = Number($('#aci_psi_e').val());
    var aci_psi_s = Number($('#aci_psi_s').val());
    var aci_psi_g = Number($('#aci_psi_g').val());
    var cb = Number($('#tbl_cb').html());
    var ktr = Number($('#tbl_ktr').html());
    var Ld = 0;
    var Lda = 0;

    //ACI 318-19 25.4.1.4 root(F'c) shall not exceed 100
    var sqrtfpc = Math.min(100,Math.sqrt(fpc_psi));

    //ACI 318-19 25.4.2.4b (cb+Ktr)/db shall not exceed 2.5
    var confine_calc = (cb+ktr)/db;
    var confine = Math.min(confine_calc,2.5);
    
    $('#TBL_CONFINE_EQUATION').html('\\[\\frac{c_{b}+K_{tr}}{d_{b}} = \\text{min}\\begin{bmatrix}\\frac{'+ cb.toFixed(2).toString()+'+'+ ktr.toFixed(2).toString() +'}{'+ db.toFixed(3).toString()+'}\\\\ 2.5 \\end{bmatrix} = \\text{min}\\begin{bmatrix}'+ confine_calc.toFixed(2).toString()+'\\\\ 2.5 \\end{bmatrix} ='+ confine.toFixed(3).toString() +' \\text{ [25.4.2.4]}\\]');

    //ACI 318-19 equation (25.4.2.4a)
    var psi_et = Math.min(aci_psi_e*aci_psi_t, 1.7);

    Lda = ((3/40)*(fy_psi/(lambda*sqrtfpc))*((psi_et*aci_psi_s*aci_psi_g)/confine))*db;
    Ld = Math.max(Lda,12);

    //$('#Ld').html(Ld.toFixed(3).toString());
    $('#Ld_LINK').html("ACI 318-19 Tension Development Length</br>L<sub>d</sub>= "+ Ld.toFixed(3).toString()+" in");

    if (psi_et == 1.7){
        $('#TBL_LD_A_EQUATION').html('\\[\\left( \\frac{3}{40} \\frac{f_{y}}{\\lambda\\sqrt{f\'_{c}}} \\frac{\\psi_{t}\\psi_{e}\\psi_{s}\\psi_{g}}{(\\frac{c_{b}+K_{tr}}{d_{b}})} \\right) d_{b} = \\left( \\frac{3}{40} \\frac{'+ fy_psi.toFixed(2).toString()+'}{('+ lambda.toFixed(2).toString()+')('+ sqrtfpc.toFixed(2).toString()+')}'
        + '\\frac{(1.7)('+ aci_psi_s.toFixed(2).toString()+')('+ aci_psi_g.toFixed(2).toString()+')}'
        + '{('+ confine.toFixed(2).toString()+')} \\right) '+ db.toFixed(3).toString()+' = '+ Lda.toFixed(3).toString()+'\\text{ in (25.4.2.4a)}, \\text{ where }\\psi_t\\psi_e\\text{ need not exceed }1.7\\]');
    } else {
        $('#TBL_LD_A_EQUATION').html('\\[\\left( \\frac{3}{40} \\frac{f_{y}}{\\lambda\\sqrt{f\'_{c}}} \\frac{\\psi_{t}\\psi_{e}\\psi_{s}\\psi_{g}}{(\\frac{c_{b}+K_{tr}}{d_{b}})} \\right) d_{b} = \\left( \\frac{3}{40} \\frac{'+ fy_psi.toFixed(2).toString()+'}{('+ lambda.toFixed(2).toString()+')('+ sqrtfpc.toFixed(2).toString()+')}'
        + '\\frac{('+ aci_psi_t.toFixed(2).toString()+')('+ aci_psi_e.toFixed(2).toString()+')('+ aci_psi_s.toFixed(2).toString()+')('+ aci_psi_g.toFixed(2).toString()+')}'
        + '{('+ confine.toFixed(2).toString()+')} \\right) '+ db.toFixed(3).toString()+' = '+ Lda.toFixed(3).toString()+'\\text{ in (25.4.2.4a)}\\]');
    }


    $('#TBL_LD_EQUATION').html('\\[L_{d} = \\text{max } \\begin{bmatrix}'+ Lda.toFixed(3).toString()+'\\text{ in} \\\\ 12 \\text{ in} \\end{bmatrix} = '+ Ld.toFixed(3).toString()+'\\text{ in}\\]');

    MathJax.typesetPromise().then(()=>{});
};

//Function to compute Ldh
function compute_Ldh(){
    var db = Number($('#tbl_db').html());
    var lambda = Number($('#aci_lambda').val());
    var fpc_psi = Number($('#fpc_psi').val());
    var fy_psi = Number($('#fy_psi').val());
    var aci_psi_e = Number($('#aci_psi_e_ldh').val());
    var aci_psi_c = Number($('#aci_psi_c_ldh').val());
    var aci_psi_r = Number($('#aci_psi_r_ldh').val());
    var aci_psi_o= Number($('#aci_psi_o_ldh').val());
    var bend_dia_in = 0;
    var bend_dia_in_outside = 0;
    var bend_radius_in = 0;
    var bend_radius_in_outside = 0;
    var l_ext_90  = 0;
    var l_ext_180 = 0;
    
    //ACI 318-19 25.4.1.4 root(F'c) shall not exceed 100
    var sqrtfpc = Math.min(100,Math.sqrt(fpc_psi));


    //ACI 318-19 25.4.3.1(a)
    var ldh_a = ((fy_psi*aci_psi_e*aci_psi_r*aci_psi_o*aci_psi_c)/(55*lambda*sqrtfpc))*Math.pow(db,1.5);
    var ldh_b = 8*db;

    $('#TBL_LDHA_EQUATION').html('\\[\\left(\\frac{f_{y}\\psi_{e}\\psi_{r}\\psi_{o}\\psi_{c}}{55\\lambda\\sqrt{f\'_{c}}} \\right)d_{b}^{1.5} = '
                                + '\\left(\\frac{('+ fy_psi.toFixed(2).toString()+')('+ aci_psi_e.toFixed(2).toString()+')('+ aci_psi_r.toFixed(2).toString()+')('+ aci_psi_o.toFixed(2).toString()+')('+ aci_psi_c.toFixed(4).toString()+')}{55('+ lambda.toFixed(2).toString()+')('+ sqrtfpc.toFixed(2).toString()+')} \\right)'+ db.toFixed(3).toString()+'^{1.5}'
                                + '= '+ ldh_a.toFixed(3).toString()+' \\text{ in}\\]');

    //ACI 318-14 25.4.3.1 -- Ldh is max of (a),(b), and (c)
    var Ldh = Math.max(ldh_a,ldh_b,6);

    //$('#Ldh').html(Ldh.toFixed(3).toString());
    $('#Ldh_LINK').html("ACI 318-19 Hooked Development Length</br>L<sub>dh</sub>= "+ Ldh.toFixed(3).toString()+" in");

    $('#TBL_LDH_EQUATION').html('\\[L_{dh} = \\text{max }\\begin{bmatrix}\\text{(a) } '+ ldh_a.toFixed(3).toString()+' \\\\ \\text{(b) } '+ ldh_b.toFixed(3).toString()+'\\\\ \\text{(c) }6 \\text{ in} \\end{bmatrix} = '+ Ldh.toFixed(3).toString()+' \\text{ in [25.4.3.1]} \\]');

    MathJax.typesetPromise().then(()=>{});

    //Bend diameters and Lext from Table 25.3.1
    if(db>1.410){
        bend_dia_in = 10*db;
        l_ext_90 = 12*db;
        l_ext_180 = Math.max(2.5,4*db);
    } else if(db>1.000 && db<1.693){
        bend_dia_in = 8*db;
        l_ext_90 = 12*db;
        l_ext_180 = Math.max(2.5,4*db);
    } else{
        bend_dia_in = 6*db;
        l_ext_90 = 12*db;
        l_ext_180 = Math.max(2.5,4*db);
    }

    bend_radius_in = bend_dia_in*0.5;
    bend_radius_in_outside = bend_radius_in + db;
    bend_dia_in_outside = bend_dia_in + (2*db);

    $('#aci_90_bend').html('&#x2300;<sub>inner</sub> = '+ bend_dia_in.toFixed(3).toString()+' in</br>r<sub>inner</sub> = '+ bend_radius_in.toFixed(3).toString()+' in</br>&#x2300;<sub>outer</sub> = '+ bend_dia_in_outside.toFixed(3).toString()+' in</br>r<sub>outer</sub> = '+ bend_radius_in_outside.toFixed(3).toString()+' in</br>L<sub>ext</sub> = '+ l_ext_90.toFixed(3).toString()+' in');
    $('#aci_180_bend').html('&#x2300;<sub>inner</sub> = '+ bend_dia_in.toFixed(3).toString()+' in</br>r<sub>inner</sub> = '+ bend_radius_in.toFixed(3).toString()+' in</br>&#x2300;<sub>outer</sub> = '+ bend_dia_in_outside.toFixed(3).toString()+' in</br>r<sub>outer</sub> = '+ bend_radius_in_outside.toFixed(3).toString()+' in</br>L<sub>ext</sub> = '+ l_ext_180.toFixed(3).toString()+' in');
};

function gradeChange(){

    var fy_psi = Number($('#fy_psi').val());

    if (fy_psi == 100000){
        $("#aci_psi_g option[value='1.3']").prop('selected',true);
        $("#psi_g_text").html("Grade 100");
    } else if (fy_psi == 80000){
        $("#aci_psi_g option[value='1.15']").prop('selected',true);
        $("#psi_g_text").html("Grade 80");
    } else {
        $("#aci_psi_g option[value='1.0']").prop('selected',true);
        $("#psi_g_text").html("Grade 40 or Grade 60");
    }

    compute_Ld();
    compute_Ldh();
};

function positionChange(){
    var aci_psi_t = Number($('#aci_psi_t').val());

    if (aci_psi_t == 1.3){
        $("#psi_t_text").html("More than 12 in. of fresh concrete placed below horizontal reinforcement.");
    } else {
        $("#psi_t_text").html("Other");
    }

    compute_Ld();
};

function epoxyChangeLd(){
    var aci_psi_e = Number($('#aci_psi_e').val());

    if (aci_psi_e == 1.5){
        $("#psi_e_text").html("Epoxy-coated or zinc and epoxy dual-coated reinforcement with clear cover less than 3d<sub>b</sub> or clear spacing less than 6d<sub>b</sub>");
    } else if (aci_psi_e == 1.2){
        $("#psi_e_text").html("Epoxy-coated or zinc and epoxy dual-coated reinforcement for all other conditions.");
    } else {
        $("#psi_e_text").html("Uncoated of zinc-coated(galvanized) reinforcement.");
    }

    compute_Ld();
};

function epoxyChangeLdh(){
    var aci_psi_e_ldh = Number($('#aci_psi_e_ldh').val());

    if (aci_psi_e_ldh == 1.2){
        $("#psi_e_ldh_text").html("Epoxy-coated or zinc and epoxy dual-coated reinforcement.");
    } else {
        $("#psi_e_ldh_text").html("Uncoated or zinc-coated (galvanized) reinforcement");
    }

    compute_Ldh();
};

function confineChangeLdh(){
    var aci_psi_r_ldh = Number($('#aci_psi_r_ldh').val());

    if (aci_psi_r_ldh == 1.0){
        $("#psi_r_ldh_text").html("For No. 11 and smaller bars with A<sub>th</sub>&GreaterEqual;0.4A<sub>hs</sub> or s&GreaterEqual;6d<sub>b</sub>.");
    } else {
        $("#psi_r_ldh_text").html("Other");
    }

    compute_Ldh();
};

function locationChangeLdh(){
    var aci_psi_o_ldh = Number($('#aci_psi_o_ldh').val());

    if (aci_psi_o_ldh == 1.0){
        $("#psi_o_ldh_text").html("For No. 11 and smaller diameter hooked bars: (1)Terminating inside column core with side cover normal to plane of hook&GreaterEqual;2.5in., or (2) With side cover normal to plane of hook&GreaterEqual;6d<sub>b</sub>.");
    } else {
        $("#psi_o_ldh_text").html("Other");
    }

    compute_Ldh();
};

function fpcChange(){

    var fpc_psi = Number($('#fpc_psi').val());

    if (fpc_psi < 6000) {
        let psi_c = (fpc_psi/15000) + 0.6

        $('#aci_psi_c_ldh').val(psi_c.toFixed(4).toString());
        $("#psi_c_ldh_text").html("f<sup>'</sup><sub>c</sub>&lt;6,000 psi = f<sup>'</sup><sub>c</sub>/15,000 + 0.6");

    } else {
        $('#aci_psi_c_ldh').val("1.0");
        $("#psi_c_ldh_text").html("f<sup>'</sup><sub>c</sub>&GreaterEqual;6,000 psi");
    }

    compute_Ldh();
    compute_Ld();
}

// This function is used for event handlers after the HTML document loads
function main() {

    // run computations after page load
    fpcChange();

    //force a Ktr change event
    $(function () {
        $(".ktr_watch").change();
    });

    //On bar selection populate bar diameter
    // and set the Psi_S option
    $("#aci_bar").on("change",function(){
        var db = $('#aci_bar').find(":selected").val();
        var db_as_number = Number(db);

        $('#tbl_db').html(db);

        if (db_as_number > 0.75){
            $("#aci_psi_s option[value='1.0']").prop('selected',true);
            $("#psi_s_text").html("No. 7 and larger bars.");
        } else {
            $("#aci_psi_s option[value='0.8']").prop('selected',true);
            $("#psi_s_text").html("No. 6 and smaller bars and deformed wires.")
        }
        
        compute_Ld();
        compute_Ldh();
    });

    //On Cc or Sb change recompute Cb
    $('.cb_watch').on("change",function(){

        var half_s = 0.5*Number($('#sb_in').val());
        var cc = Number($('#cc_in').val());

        var cb = Math.min(half_s,cc);

        $('#tbl_cb').html(cb);
        
        compute_Ld();
    });

    //Recompute Ktr if Atr,s,or n changes
    $('.ktr_watch').on("change",function(){
        var Atr = Number($('#atr_in2').val());
        var s = Number($('#s_in').val());
        var n = Number($('#n_bars').val());
        var ktr = 0

        if (Atr===0 || s===0 || n===0){
                ktr = 0
        } else{

            //ACI 318-14 equation (25.4.2.3b)
            ktr = (40*Atr)/(s*n)
        }

        $('#tbl_ktr').html(ktr.toFixed(3));
        $('#TBL_KTR_EQUATION').html('\\[K_{tr} = \\frac{40 A_{tr}}{sn} = \\frac{40('+ Atr.toFixed(2).toString()+ ')}{('+ s.toFixed(2).toString() +')('+ n.toFixed(2).toString() +')} ='+ ktr.toFixed(3).toString() +' \\text{ (25.4.2.4b)}  \\]');
        MathJax.typesetPromise().then(()=>{});

        compute_Ld();
    });

    // On any input change recompute Ld
    $('.input-sm').on("change", function(){
        compute_Ld();
        compute_Ldh();
    });



};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
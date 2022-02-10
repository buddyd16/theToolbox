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

    //global variable to note if a calc has been run
    var has_run = false;

    //compute d from default values
    compute_d();
    compute_nuc_design();

    // run calcs on button press
    $("#btn_calc").click(function(){

        compute_d();
        compute_nuc_design();
        verify_16_5();
        check_dimensions();
        Compute_steel_areas();
        has_run = true;
    });

    // run calcs on input change
    $(".user_param").on("change",function(){
        
        clear_results();

    });

    //On bar selection populate bar diameter and area
    $("#aci_bar_main").on("change",function(){
        var bar = Number($('#aci_bar_main').find(":selected").val());
        
        var bar_info = ACI_Bars[bar];

        var bar_d_in = bar_info[0];
        var bar_as_in2 = bar_info[1];

        $('#tbl_db_main').html(bar_d_in);
        $('#tbl_as_main').html(bar_as_in2);

    });

    $("#aci_bar_tie").on("change",function(){
        var bar = Number($('#aci_bar_tie').find(":selected").val());
        
        var bar_info = ACI_Bars[bar];

        var bar_d_in = bar_info[0];
        var bar_as_in2 = bar_info[1];

        $('#tbl_db_tie').html(bar_d_in);
        $('#tbl_as_tie').html(bar_as_in2);

    });

    $("#fc_psi").on("change",function(){
        
        var fc_psi = Number($('#fc_psi').val());
        
        var beta1 = ACI_Beta1(fc_psi);

        $('#tbl_beta1').html(beta1.toFixed(3));

    });

    function compute_nuc_design(){
        var nuc_kips = Number($('#nuc_kips').val());
        var vuc_kips = Number($('#vuc_kips').val());
        var nuc_min = 0.2*vuc_kips;

        if (nuc_kips < nuc_min){
            $('#tbl_nuc_design_kips').html(nuc_min.toFixed(3));
        } else {
            $('#tbl_nuc_design_kips').html(nuc_kips.toFixed(3));
        }
        
        var H_in = Number($('#Hc_in').val());
        var d_in = Number($('#tbl_d_in').html());
        var av_in = Number($('#av_in').val());
        //also compute Mu design in this step
        //Vu av + Nu (H-d) (1/12)
        var nuc_des = Math.max(nuc_min,nuc_kips);
        var mu_des = ((vuc_kips*av_in)+(nuc_des*(H_in-d_in)))*(1/12);

        $('#tbl_mu_design_ftkips').html(mu_des.toFixed(3));

    };

    function compute_d(){
        var bar = Number($('#aci_bar_main').find(":selected").val());
        var bar_info = ACI_Bars[bar];
        var bar_d_in = bar_info[0];
        var bar_as_in2 = bar_info[1];

        //Compute the depth to tension steel, d
        var cover_in = Number($('#cover_in').val());
        var H_in = Number($('#Hc_in').val());
        var d_in = H_in - (cover_in + (bar_d_in/2.0));

        $('#tbl_d_in').html(d_in.toFixed(3));

    };

    function verify_16_5(){
        var d = Number($('#tbl_d_in').html());
        var av = Number($('#av_in').val());
        var av_d = av/d;
        var nuc_kips = Number($('#nuc_kips').val());
        var vuc_kips = Number($('#vuc_kips').val());

        if (av_d <= 1){

            $('#av_d_test').html('\\[ \\frac{'+av.toFixed(3).toString()+'}{'+d.toFixed(3).toString()+'} = '+av_d.toFixed(3).toString()+' \\le 1.0  \\]');
            $('#av_d_test_result').html("<strong>OK</strong>");
            $('#av_d_test_row').removeClass("table-danger");
            $('#av_d_test_row').addClass("table-success");

        } else {
            $('#av_d_test').html('\\[ \\frac{'+av.toFixed(3).toString()+'}{'+d.toFixed(3).toString()+'} = '+av_d.toFixed(3).toString()+' \\gt 1.0  \\]');
            $('#av_d_test_result').html("<strong>NG</strong>");
            $('#av_d_test_row').removeClass("table-success");
            $('#av_d_test_row').addClass("table-danger");
        }

        if (nuc_kips<=vuc_kips){
            $('#nv_test').html('\\[ '+nuc_kips.toFixed(3).toString()+'\\le'+vuc_kips.toFixed(3).toString()+' \\]');
            $('#nv_test_result').html("<strong>OK</strong>");
            $('#nv_test_row').removeClass("table-danger");
            $('#nv_test_row').addClass("table-success");
        } else {
            $('#nv_test').html('\\[ '+nuc_kips.toFixed(3).toString()+'\\gt'+vuc_kips.toFixed(3).toString()+' \\]');
            $('#nv_test_result').html("<strong>NG</strong>");
            $('#nv_test_row').removeClass("table-success");
            $('#nv_test_row').addClass("table-danger");
        }

        if (av_d <=1 && nuc_kips<=vuc_kips){
            $('#status_165_test').html("OK");
            $('#status_165_test').removeClass("table-danger");
            $('#status_165_test').addClass("table-success");

            $('#res_status_16511_value').html("<strong>OK</strong>");
            $('#res_status_16511').removeClass("table-danger");
            $('#res_status_16511').addClass("table-success");

            // everything checked out 16.5 is applicable next
            // check the dimensions
            

        } else {
            $('#status_165_test').html("NG");
            $('#status_165_test').removeClass("table-success");
            $('#status_165_test').addClass("table-danger");

            $('#res_status_16511_value').html("<strong>NG</strong>");
            $('#res_status_16511').removeClass("table-success");
            $('#res_status_16511').addClass("table-danger");
        }

        MathJax.typesetPromise().then(()=>{});
    };

    function check_dimensions(){
        var weight = Number($('#aci_lambda').find(":selected").val());
        var fc_psi = Number($('#fc_psi').val());
        var bw_in = Number($('#Bc_in').val());
        var d_in = Number($('#tbl_d_in').html());
        var av_in = Number($('#av_in').val());
        var vuc_kips = Number($('#vuc_kips').val());
        var phi = Number($('#phi_corbel').html());
        var vu_phi_lbs = (vuc_kips*1000)/phi;

        if (weight == 1){

            // normalweight concrete check against 16.5.2.4
            $('#dimension_check_section').html("<u><strong>16.5.2.4 -- Verification that dimensions satisfy max shear friction</strong></u>");
            $('#dimension_check_a_formula').html("\\[0.2F'_{c}b_{w}d \\]");
            $('#dimension_check_b_formula').html("\\[(480+0.08F'_{c})b_{w}d \\]");
            $('#dimension_check_c_formula').html("\\[1600b_{w}d \\]");

            var a = 0.2*fc_psi*bw_in*d_in;
            var a_jax = '\\[0.2 ('+fc_psi.toFixed(2).toString()+')('+bw_in.toFixed(2).toString()+')('+d_in.toFixed(3).toString()+') = '+a.toFixed(2).toString()+' \\text{ lbs}';
            var b = (480+(0.08*fc_psi))*bw_in*d_in;
            var b_jax = '\\[(480+0.08('+fc_psi.toFixed(2).toString()+'))('+bw_in.toFixed(2).toString()+')('+d_in.toFixed(3).toString() +')= '+b.toFixed(2).toString()+' \\text{ lbs}';
            var c = 1600*bw_in*d_in;
            var c_jax = '\\[1600('+bw_in.toFixed(2).toString()+')('+d_in.toFixed(3).toString()+')= '+c.toFixed(2).toString()+' \\text{ lbs}';
            var abc = [a,b,c];
            var abctest = [a>=vu_phi_lbs,b>=vu_phi_lbs,c>=vu_phi_lbs];

            if (a>=vu_phi_lbs){
                $('#dimension_check_a_evaluation').html(a_jax+'\\ge \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_a_status').html("<strong>OK</strong>");
                $('#dimension_check_a_row').removeClass("table-danger");
                $('#dimension_check_a_row').addClass("table-success");
            } else {
                $('#dimension_check_a_evaluation').html(a_jax+'\\lt \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_a_status').html("<strong>NG</strong>");
                $('#dimension_check_a_row').removeClass("table-success");
                $('#dimension_check_a_row').addClass("table-danger");
            }

            if (b>=vu_phi_lbs){
                $('#dimension_check_b_evaluation').html(b_jax+'\\ge \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_b_status').html("<strong>OK</strong>");
                $('#dimension_check_b_row').removeClass("table-danger");
                $('#dimension_check_b_row').addClass("table-success");
            } else {
                $('#dimension_check_b_evaluation').html(b_jax+'\\lt \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_b_status').html("<strong>NG</strong>");
                $('#dimension_check_b_row').removeClass("table-success");
                $('#dimension_check_b_row').addClass("table-danger");
            }

            if (c>=vu_phi_lbs){
                $('#dimension_check_c_evaluation').html(c_jax+'\\ge \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_c_status').html("<strong>OK</strong>");
                $('#dimension_check_c_row').removeClass("table-danger");
                $('#dimension_check_c_row').addClass("table-success");
            } else {
                $('#dimension_check_c_evaluation').html(c_jax+'\\lt \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_c_status').html("<strong>NG</strong>");
                $('#dimension_check_c_row').removeClass("table-success");
                $('#dimension_check_c_row').addClass("table-danger");
            }
            
            if(abctest.every(Boolean)){
                $('#dimension_check_test').html("OK");
                $('#dimension_check_test').removeClass("table-danger");
                $('#dimension_check_test').addClass("table-success");

                $('#res_status_16524_value').html("<strong>OK</strong>");
                $('#res_status_16524').removeClass("table-danger");
                $('#res_status_16524').addClass("table-success");

            } else {

                $('#dimension_check_test').html("NG");
                $('#dimension_check_test').removeClass("table-success");
                $('#dimension_check_test').addClass("table-danger");

                $('#res_status_16524_value').html("<strong>NG</strong>");
                $('#res_status_16524').removeClass("table-success");
                $('#res_status_16524').addClass("table-danger");
            }

        } else {
            // lightweight concrete check against 16.5.2.5
            $('#dimension_check_section').html("<u><strong>16.5.2.5 -- Verification that dimensions satisfy max shear friction</strong></u>");
            $('#dimension_check_c_formula').html("");
            $('#dimension_check_c_evaluation').html("");
            $('#dimension_check_c_status').html("");
            $('#dimension_check_c_row').removeClass("table-success");
            $('#dimension_check_c_row').removeClass("table-danger");
            $('#dimension_check_a_formula').html("\\[(0.2-(0.07\\frac{a_{v}}{d}))F'_{c}b_{w}d \\]");
            $('#dimension_check_b_formula').html("\\[(800-(280\\frac{a_{v}}{d}))b_{w}d \\]");

            var a = (0.2-(0.07*(av_in/d_in)))*fc_psi*bw_in*d_in;
            var a_jax = '\\[(0.2-(0.07\\frac{'+av_in.toFixed(3).toString()+'}{'+d_in.toFixed(3).toString()+'}))('+fc_psi.toFixed(2).toString()+')('+bw_in.toFixed(2).toString()+')('+d_in.toFixed(3).toString()+') = '+a.toFixed(2).toString()+' \\text{ lbs}';
            var b = (800-(280*(av_in/d_in)))*bw_in*d_in;
            var b_jax = '\\[(800-(280\\frac{'+av_in.toFixed(3).toString()+'}{'+d_in.toFixed(3).toString()+'}))('+bw_in.toFixed(2).toString()+')('+d_in.toFixed(3).toString()+') = '+b.toFixed(2).toString()+' \\text{ lbs}';

            var ab = [a,b];
            var abtest = [a>=vu_phi_lbs,b>=vu_phi_lbs];

            if (a>=vu_phi_lbs){
                $('#dimension_check_a_evaluation').html(a_jax+'\\ge \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_a_status').html("<strong>OK</strong>");
                $('#dimension_check_a_row').removeClass("table-danger");
                $('#dimension_check_a_row').addClass("table-success");
            } else {
                $('#dimension_check_a_evaluation').html(a_jax+'\\lt \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_a_status').html("<strong>NG</strong>");
                $('#dimension_check_a_row').removeClass("table-success");
                $('#dimension_check_a_row').addClass("table-danger");
            }

            if (b>=vu_phi_lbs){
                $('#dimension_check_b_evaluation').html(b_jax+'\\ge \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_b_status').html("<strong>OK</strong>");
                $('#dimension_check_b_row').removeClass("table-danger");
                $('#dimension_check_b_row').addClass("table-success");
            } else {
                $('#dimension_check_b_evaluation').html(b_jax+'\\lt \\frac{V_{uc}(1000)}{\\phi}= '+ vu_phi_lbs.toFixed(2).toString()+' \\text{ lbs} \\]');
                $('#dimension_check_b_status').html("<strong>NG</strong>");
                $('#dimension_check_b_row').removeClass("table-success");
                $('#dimension_check_b_row').addClass("table-danger");
            }

            if(abtest.every(Boolean)){
                $('#dimension_check_test').html("OK");
                $('#dimension_check_test').removeClass("table-danger");
                $('#dimension_check_test').addClass("table-success");

                $('#res_status_16524_value').html("<strong>OK</strong>");
                $('#res_status_16524').removeClass("table-danger");
                $('#res_status_16524').addClass("table-success");

            } else {

                $('#dimension_check_test').html("NG");
                $('#dimension_check_test').removeClass("table-success");
                $('#dimension_check_test').addClass("table-danger");

                $('#res_status_16524_value').html("<strong>NG</strong>");
                $('#res_status_16524').removeClass("table-success");
                $('#res_status_16524').addClass("table-danger");
            }
        }
        MathJax.typesetPromise().then(()=>{});
    };

    function Compute_steel_areas(){
        var fy_psi = Number($('#fy_psi').val());
        var lambda = Number($('#aci_lambda').find(":selected").val());
        var fc_psi = Number($('#fc_psi').val());
        var bw_in = Number($('#Bc_in').val());
        var d_in = Number($('#tbl_d_in').html());
        var av_in = Number($('#av_in').val());
        var vuc_kips = Number($('#vuc_kips').val());
        var nuc_design_kips = Number($('#tbl_nuc_design_kips').html());
        var phi = Number($('#phi_corbel').html());
        var mu = Number($('#aci_mu').find(":selected").val());
        var mu_ftkips = Number($('#tbl_mu_design_ftkips').html());
        var beta1 = ACI_Beta1(fc_psi);

        // 16.5.4.3 - direct tension steel (eq 16.5.4.3)

        var an_in2 = (nuc_design_kips*1000)/(phi*fy_psi);

        $('#tbl_an_tension').html(an_in2.toFixed(3).toString());

        //16.5.4.4 - steel for shear friction

        var avf_in2 = (vuc_kips*1000)/(phi*mu*lambda*fy_psi);
        
        $('#tbl_avf_shearfriction').html(avf_in2.toFixed(3).toString());

        //16.5.4.5 - steel for flexure following assumptions in 22.2

        //Quadratic Formula for solution of Af
        var A = (-1*15.0*fy_psi*fy_psi)/(34.0*fc_psi*bw_in);
        var B = (3.0*fy_psi*d_in)/4.0;
        var C = mu_ftkips*12.0*-1000.0;

        // check that A is non-zero and that there is not a negative within
        // the square root.
        if (A==0 || (B*B)-(4*A*C) < 0 ){
            var af_quadratic = [1000,1000];
            var af_in2 = 1000.0;
        } else {
            var af_quadratic = [(-B + Math.sqrt((B*B)-(4*A*C)))/(2*A),(-B - Math.sqrt((B*B)-(4*A*C)))/(2*A)];
            var af_in2 = Math.min(...af_quadratic);
        }

        $('#tbl_af_req').html(af_in2.toFixed(3).toString());

        // upper limit on Af for a tension controlled section et=0.004

        var af_max_in2 = (51*fc_psi*bw_in*beta1*d_in)/(140*fy_psi);

        if (af_in2>af_max_in2){
            $('#res_status_aflimit_value').html("<strong>NG</strong>");
            $('#res_status_aflimit').removeClass("table-success");
            $('#res_status_aflimit').addClass("table-danger");
        } else {
            $('#res_status_aflimit_value').html("<strong>OK</strong>");
            $('#res_status_aflimit').removeClass("table-danger");
            $('#res_status_aflimit').addClass("table-success");
        }

        $('#tbl_af_max').html(af_max_in2.toFixed(3).toString());

        // 16.5.5.1 -- Asc, primary tension reinf. computations

        var asc_jax = '\\[ \\text{max } \\begin{bmatrix}A_{f}+A_{n} \\\\ (\\frac{2}{3})A_{vf}+A_{n} \\\\ 0.04(\\frac{f\'_{c}}{f_{y}})(B_{c}d) \\end{bmatrix} = \
                            \\text{max } \\begin{bmatrix}'+af_in2.toFixed(3).toString()+'+'+ an_in2.toFixed(3).toString() +' \\\\ (\
                                \\frac{2}{3})('+avf_in2.toFixed(3).toString()+')+'+ an_in2.toFixed(3).toString() +' \\\\ \
                                0.04(\\frac{'+fc_psi.toFixed(2).toString()+'}{'+fy_psi.toFixed(2).toString()+'})(('+bw_in.toFixed(2).toString()+')('+d_in.toFixed(2).toString()+')) \\end{bmatrix}=';
        
        var asc_a = af_in2+an_in2;
        var asc_b = ((2/3)*avf_in2)+an_in2;
        var asc_c = 0.04*(fc_psi/fy_psi)*(bw_in*d_in);

        var asc_in2 = Math.max(asc_a,asc_b,asc_c);

        var asc_jax_full = asc_jax + '\\text{max } \\begin{bmatrix}'+asc_a.toFixed(3).toString()+' \\\\ '+asc_b.toFixed(3).toString()+' \\\\ '+asc_c.toFixed(3).toString()+'\\end{bmatrix} \\]';

        $('#tbl_asc_mathjax').html(asc_jax_full);
        $('#tbl_asc_value').html(asc_in2.toFixed(3).toString());

        $('#res_asc_value').html(asc_in2.toFixed(3).toString());

        var bar = Number($('#aci_bar_main').find(":selected").val());
        
        var bar_info = ACI_Bars[bar];

        var bar_d_in = bar_info[0];
        var bar_as_in2 = bar_info[1];

        var num_main = Math.ceil(asc_in2 / bar_as_in2);
        var as_main_in2 = num_main*bar_as_in2;

        $('#res_num_main_bars').html('<strong>&there4; use ('+num_main.toString()+')#'+bar.toString()+' - A<sub>sc</sub> :</strong>');
        $('#res_asc_provided').html(as_main_in2.toFixed(3).toString());
        
        // 16.5.5.2 -- Ah, are of closed stirrups or ties parallel to Asc computations
        var ah_in2 = 0.5*(asc_in2-an_in2);

        var ah_mathjax = '\\[A_{h}=0.5(A_{sc}-A_{n}) = 0.5('+asc_in2.toFixed(3).toString()+' - '+an_in2.toFixed(3).toString()+') \\]'
        
        $('#tbl_ah_mathjax').html(ah_mathjax);
        $('#tbl_ah_value').html(ah_in2.toFixed(3).toString());

        var tiebar = Number($('#aci_bar_tie').find(":selected").val());
        
        var tiebar_info = ACI_Bars[tiebar];

        var tiebar_d_in = tiebar_info[0];
        var tiebar_as_in2 = tiebar_info[1];

        $('#res_ah_value').html(ah_in2.toFixed(3).toString());

        var num_ties = Math.ceil(ah_in2/ (2*tiebar_as_in2));
        var as_ties_in2 = num_ties*tiebar_as_in2*2;

        $('#res_num_tie_bars').html('<strong> &there4; use ('+num_ties.toString()+')#'+tiebar.toString()+' (2-Legs Assumed) - A<sub>h</sub> :</strong>');
        $('#res_ah_provided').html(as_ties_in2.toFixed(3).toString());

        MathJax.typesetPromise().then(()=>{});

        update_chart(num_ties);
    };

    function clear_results(){

        if (has_run){
            $('#res_status_16511_value').html("--");
            $('#res_status_16511').removeClass("table-success");
            $('#res_status_16511').removeClass("table-danger");
            $('#res_status_16524_value').html("--");
            $('#res_status_16524').removeClass("table-success");
            $('#res_status_16524').removeClass("table-danger");
            $('#res_status_aflimit_value').html("--");
            $('#res_status_aflimit').removeClass("table-danger");
            $('#res_status_aflimit').removeClass("table-success");
            $('#res_asc_value').html("--");
            $('#res_num_main_bars').html("--");
            $('#res_asc_provided').html("--");
            $('#res_ah_value').html("--");
            $('#res_num_tie_bars').html("--");
            $('#res_ah_provided').html("--");
            has_run = false;
        }

    };

    function update_chart(num_ties){

        var canvas = document.getElementById("corbel_canvas");
        var ctx = canvas.getContext("2d");

        ctx.clearRect(0,0,canvas.width,canvas.height);

        var Hc_in = Number($('#Hc_in').val());
        var Lc_in = Number($('#Lc_in').val());
        var Sc_in = Number($('#Sc_in').val());
        var d_in = Number($('#tbl_d_in').html()); 

        var xsf = 200/(Lc_in+Sc_in);
        var ysf = 390/Hc_in;

        var sf = Math.min(xsf,ysf);

        //outline the corbel
        
        ctx.beginPath();
        
        ctx.moveTo(395,5);
        var x = 395-(sf*Sc_in);
        ctx.lineTo(x,5);
        ctx.lineTo(x,105);
        var pt3 = [x,105];
        x = x - (sf*Lc_in);
        ctx.lineTo(x,105);
        var y = 105 + (d_in*0.5*sf);
        var pt4 = [x,105];
        var pt5 = [x,y];
        ctx.lineTo(x,y);
        x = 395-(sf*Sc_in);
        y = 105 + (Hc_in*sf);
        var pt6 = [x,y];
        ctx.lineTo(x,y);
        ctx.lineTo(x,595);
        ctx.lineTo(395,595);
        
        ctx.closePath();

        ctx.fillStyle = "#bfbfbf";
        ctx.fill();
        

        //tie bar
        var cover = Number($('#cover_in').val());
        var bar = Number($('#aci_bar_main').find(":selected").val());
        var bar_info = ACI_Bars[bar];
        var bar_d_in = bar_info[0];

        var tiebar = Number($('#aci_bar_tie').find(":selected").val());
        var tiebar_info = ACI_Bars[tiebar];
        var tiebar_d_in = tiebar_info[0];

        var tie_x = pt4[0] + ((sf)*(cover+(4/8)+tiebar_d_in+(0.5*bar_d_in)));
        var tie_y = pt4[1] + ((sf)*(cover+bar_d_in+(0.5*bar_d_in)));
        var tie_r = (bar_d_in*0.5)*sf;

        ctx.beginPath();
        
        ctx.arc(tie_x,tie_y,tie_r,0,2*Math.PI,false);
        
        ctx.closePath();

        ctx.fillStyle = "#ff0000";
        ctx.fill();
        ctx.lineCap = "butt";
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#000000";
        ctx.stroke();

        //framing bar
        //assume #4 bar
        var frame_x1 = pt4[0] + (sf*cover);
        var frame_y1 = pt4[1] + (sf*cover);

        var uv = PerpOfLine(pt5[0],pt5[1],pt6[0],pt6[1]);

        var shift = [uv[0]*(sf*(cover+(4/16))),uv[1]*(sf*(cover+(4/16)))];

        var thick = sf*(4/8);

        var frame_xt = pt5[0] - shift[0];
        var frame_yt = pt5[1] - shift[1];
        var frame_x3 = pt6[0] - shift[0];
        var frame_y3 = pt6[1] - shift[1];

        var frame_y2 = yAtX(frame_xt,frame_yt,frame_x3,frame_y3,frame_x1);

        ctx.beginPath();

        ctx.moveTo(frame_x1,frame_y1);
        ctx.lineTo(frame_x1,frame_y2);
        ctx.lineTo(frame_x3,frame_y3);

        ctx.lineCap = "butt";
        ctx.lineWidth = thick;
        ctx.strokeStyle = "#8c8c8c";
        ctx.stroke();

        //main bar
        var radii = ACI_Standard_Bar_Radius(bar_info)
        var r_midline = radii[2];
        console.log(r_midline);

        var main_x1 = pt4[0] + ((sf)*(cover+(4/8)+tiebar_d_in));
        var main_y1 = pt4[1] + ((sf)*(cover+(0.5*bar_d_in)));
        var main_x2 = 395 - (sf*(cover+tiebar_d_in+r_midline));
        var main_y2 = main_y1;
        var main_yr = main_y1 + (sf*r_midline);
        var main_x3 = 395 - (sf*(cover+tiebar_d_in));
        var main_y3 = main_y2 + (sf*1.3*Hc_in);

        var bar_thick = sf*bar_d_in;

        ctx.beginPath();

        ctx.moveTo(main_x1,main_y1);
        ctx.lineTo(main_x2,main_y2);
        ctx.lineCap = "butt";
        ctx.lineWidth = bar_thick;
        ctx.strokeStyle = "#ff0000";
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(main_x2,main_yr,sf*r_midline,1.5*Math.PI,0,false);
        ctx.lineTo(main_x3,main_y3);

        ctx.lineCap = "butt";
        ctx.lineWidth = bar_thick;
        ctx.strokeStyle = "#ff0000";
        ctx.stroke();

        //tie bars

        var tie_thick = sf*tiebar_d_in;
        var spacing = (sf*(2/3)*d_in)/num_ties;

        var tie1_y1 = pt4[1]+(sf*(((2/3)*d_in)+cover+bar_d_in/2));
        var tie1_x1 = xAtY(frame_x1,frame_y2,frame_x3,frame_y3,tie1_y1)-(sf*tiebar_d_in);
        var tie1_x2 = 395 - (sf*(cover));

        ctx.beginPath();

        ctx.moveTo(tie1_x1,tie1_y1);
        ctx.lineTo(tie1_x2,tie1_y1);

        ctx.lineCap = "round";
        ctx.lineWidth = tie_thick;
        ctx.strokeStyle = "#0000ff";
        ctx.stroke();

        for (let i=0; i < (num_ties-1); i++){
            var tien_y = tie1_y1 - ((i+1)*(spacing));

            if (tien_y > frame_y2){
                var tien_x1 = xAtY(frame_x1,frame_y2,frame_x3,frame_y3,tien_y)-(sf*tiebar_d_in);
            } else {
                var tien_x1 = frame_x1 - (sf*tiebar_d_in);
            }

            ctx.beginPath();

            ctx.moveTo(tien_x1,tien_y);
            ctx.lineTo(tie1_x2,tien_y);
            
            ctx.lineCap = "round";
            ctx.lineWidth = tie_thick;
            ctx.strokeStyle = "#0000ff";
            ctx.stroke();
        }

        // Draw the joint surface condition per the mu selection
        var mu = Number($('#aci_mu').find(":selected").val());

        if (mu==0.6){
            ctx.beginPath();
            ctx.moveTo(pt3[0],pt3[1]);
            ctx.lineTo(pt6[0],pt6[1]);
            ctx.lineCap = "butt";
            ctx.lineWidth = "2";
            ctx.strokeStyle = "#000000";
            ctx.stroke();
        } else if (mu==1.0){

            var zz = sf*0.25;
            var num_zigs = ((sf*Hc_in)-4)/(sf);
            var N_zags = Math.floor(num_zigs);
            var Hz = (N_zags*sf);
            var ext_y = ((sf*Hc_in) - Hz)/2;
            console.log([N_zags,Hz,ext_y,sf*Hc_in,sf]);

            ctx.beginPath();
            ctx.moveTo(pt3[0],pt3[1]);
            var yt = pt3[1]+ext_y;
            var xt = pt3[0];
            ctx.lineTo(xt,yt);
            

            for (let i=0; i< (N_zags); i++){

                var yj = yt+(i*(sf));
                var xj = xt;

                var zig_x = xj - zz;
                var zig_y = yj + zz;

                ctx.lineTo(zig_x,zig_y)

                var zag_x = zig_x + (2*zz);
                var zag_y = zig_y + (2*zz);

                ctx.lineTo(zag_x,zag_y);

                var end_y = zag_y + zz;

                ctx.lineTo(xj,end_y);
            }

            ctx.lineTo(pt6[0],pt6[1]);

            ctx.lineCap = "butt";
            ctx.lineWidth = "1";
            ctx.strokeStyle = "#000000";
            ctx.stroke();
        }

        // draw the load arrows
        var av_in = Number($('#av_in').val());
        var vuc_kips = Number($('#vuc_kips').val());
        var nuc_design_kips = Number($('#tbl_nuc_design_kips').html());

        var load_sf = Math.min(75/vuc_kips,75/nuc_design_kips);

        var v_y = vuc_kips*load_sf;
        var n_x = nuc_design_kips*load_sf;

        var x_load = pt3[0]-(sf*av_in);
        var y_load = pt3[1];

        ctx.beginPath();
        ctx.moveTo(x_load,y_load);
        ctx.lineTo(x_load,y_load-v_y);
        ctx.lineCap = "butt";
        ctx.lineWidth = "1";
        ctx.strokeStyle = "#000000";
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(x_load-5,y_load-10);
        ctx.lineTo(x_load,y_load);
        ctx.lineTo(x_load+5,y_load-10);
        ctx.lineCap = "butt";
        ctx.lineWidth = "1";
        ctx.strokeStyle = "#000000";
        ctx.stroke();

        ctx.font = "12px Monaco";
        ctx.fillStyle = "#000000";
        ctx.textAlign = "left";
        ctx.fillText(vuc_kips.toFixed(2).toString()+' kips',x_load+1,y_load-v_y);

        ctx.beginPath();
        ctx.moveTo(x_load+10,y_load-5);
        ctx.lineTo(x_load,y_load);
        ctx.lineTo(x_load+10,y_load+5);
        ctx.lineCap = "butt";
        ctx.lineWidth = "1";
        ctx.strokeStyle = "#000000";
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(x_load,y_load);
        ctx.lineTo(x_load+n_x,y_load);
        ctx.lineCap = "butt";
        ctx.lineWidth = "1";
        ctx.strokeStyle = "#000000";
        ctx.stroke();

        ctx.font = "12px Monaco";
        ctx.fillStyle = "#000000";
        ctx.textAlign = "left";
        ctx.fillText(nuc_design_kips.toFixed(2).toString()+' kips',x_load+n_x,y_load-4);

    };
};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
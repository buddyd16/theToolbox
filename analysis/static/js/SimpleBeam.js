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

    UpdateChart();

    // Add row Below the first support that was clicked
    $("tbody").on("click", ".addSupportFirst", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        // get the current number of supports
        // need to limit the amount due to the 
        // exponential rise in patterns required
        var support_count = Number($("#interiorsupportsTable tbody tr").length);

        var $newRow =   '<tr class=\"interiorsupportRow\">' +
                    '<td class=\"interiorsupportuid\">R'+ Number($("#interiorsupportsTable tbody tr").length + 1).toString() + '</td>' +
                    '<td><input id=\"interiorSupport'+ Number($("#interiorsupportsTable tbody tr").length + 1).toString() + '\" name=\"interiorSupport\" class=\"interiorSupport input-sm\" style=\"width:65px\" type=\"number\" step=\"any\" min=\"0\" value=\"0\"></td>' +
                    '<td>ft</td>' +
                    '<td>' +
                    '<button type=\"button\" class=\"addSupport btn btn-secondary btn-success btn-sm\">' +
                    '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                    '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                    '</svg>' + 
                    '</button>' +
                    '<a href=\"#\" class=\"removeSupportButton badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
                    '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
                    '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
                    '</svg></a></td>' +
                    '</tr>';
        
        $curRow.after($newRow);
        
        //expand function to renumber the remaining supports
        tableBody.children('.interiorsupportRow').each(function(i) {
        // Renumber the row
        $(this).children("td:first").text('R'+String(i+1));
        });

        
        UpdateChart();
        
    });


    // Add row Below the support that was clicked
    $("tbody").on("click", ".addSupport", function(){
        
        // get the current number of supports
        // need to limit the amount due to the 
        // exponential rise in patterns required
        var support_count = Number($("#interiorsupportsTable tbody tr").length);


        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        var $newRow = $curRow.clone(true);
        
        $curRow.after($newRow);
        
        //expand function to renumber the remaining supports
        tableBody.children('.interiorsupportRow').each(function(i) {
        // Renumber the row
        $(this).children("td:first").text('R'+String(i+1));
        });

        UpdateChart();
        
    });


    // Removing support row that was clicked.
    $("tbody").on("click", ".removeSupportButton", function(event){
        
        // prevent the vertical scroll reset
        event.preventDefault();

        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //remove the row
        $(this).closest("tr").remove();
        
        //expand function to renumber the remaining supports
        tableBody.children('.interiorsupportRow').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('R'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Disable the overhang left if the fixed left box is checked
    $("#fixedLeft").change(function(){
        console.log(this.checked);
        console.log('hello');
        $("#overhangLeft").val('0.0');
        $("#overhangLeft").attr('disabled',this.checked);
        UpdateChart();
    });

    // Disable the overhang right if the fixed right box is checked
    $("#fixedRight").change(function(){
        $("#overhangRight").val('0.0');
        $("#overhangRight").attr('disabled',this.checked);
        UpdateChart();
    });
    
    // Add the descriptive text to the f1 decision
    $("#IBC_f1").change(function(){
        let f1 = $("#IBC_f1").val()

        if ( f1 == "1"){
            $('#IBC_f1_string').html("Public Assembly, L > 100 psf, or parking garage.")
        } else {
            $('#IBC_f1_string').html("Other L.")
        }
    });

    // Add the descriptive text to the f2 decision
    $("#IBC_f2").change(function(){
        let f2 = $("#IBC_f2").val()

        if ( f2 == "0.7"){
            $('#IBC_f2_string').html("Roof configuration does not shed snow.")
        } else {
            $('#IBC_f2_string').html("Other roof configurations.")
        }
    });


    // Add row below the first uls combindation
    $("tbody").on("click", ".addULSComboFirst", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");

        //new row
        var $newRow = '<tr class=\"ulsCombo\">' +
                        '<td class=\"ulscombouid\">U'+ Number($("#ulscomboTable tbody tr").length + 1).toString() +'</td>' +
                        '<td><input id=\"Dufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Dufactor\" class=\"Dufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"1\"></td>' +
                        '<td><input id=\"Fufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Fufactor\" class=\"Fufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Lufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Lufactor\" class=\"Lufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Hufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Hufactor\" class=\"Hufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Lrufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Lrufactor\" class=\"Lrufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Sufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Sufactor\" class=\"Sufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Rufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Rufactor\" class=\"Rufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Wxufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Wxufactor\" class=\"Wxufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Wyufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Wyufactor\" class=\"Wyufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Exufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Exufactor\" class=\"Exufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Eyufactor'+Number($("#ulscomboTable tbody tr").length + 1).toString() +'\" name=\"Eyufactor\" class=\"Eyufactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td>' +
                        '<select id="ulspattern" class="ulspattern input-sm" name="ulspattern" style="width:59px">' +
                            '<option value="1" > y </option>' +
                            '<option value="0" > n </option>' +
                        '</select>' +
                        '</td>' +
                        '<td>' +    
                        '<button type=\"button\" class=\"addULSCombo btn btn-secondary btn-success btn-sm\">' +
                        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                        '</svg>' +
                        '</button>' +
                        '<a href=\"#\" class=\"removeULSCombo badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
                        '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
                        '</svg></a>' +
                        '</td>' +
                        '</tr>';
        
        $curRow.after($newRow);

        //expand function to renumber the remaining supports
        tableBody.children('.ulsCombo').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('U'+String(i+1));
        });
        
        UpdateChart();
    });

    // Add ULS combo for each button after the first one
    $("tbody").on("click", ".addULSCombo", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        var $newRow = $curRow.clone(true);
        
        $curRow.after($newRow);
        
        //expand function to renumber the remaining supports
        tableBody.children('.ulsCombo').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text('U'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Remove a ULS combo
    $("tbody").on("click", ".removeULSCombo", function(event){
        
        // prevent the vertical scroll reset
        event.preventDefault();

        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //remove the row
        $(this).closest("tr").remove();
        
        //expand function to renumber the remaining supports
        tableBody.children('.ulsCombo').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('U'+String(i+1));
        });
        
        UpdateChart();
        
    });


    // Add row below the first service combindation
    $("tbody").on("click", ".addServiceComboFirst", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");

        //new row
        var $newRow = '<tr class=\"serviceCombo\">' +
                        '<td class=\"servicecombouid\">S'+ Number($("#servicecomboTable tbody tr").length + 1).toString() +'</td>' +
                        '<td><input id=\"Dsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Dsfactor\" class=\"Dsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"1\"></td>' +
                        '<td><input id=\"Fsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Fsfactor\" class=\"Fsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Lsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Lsfactor\" class=\"Lsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Hsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Hsfactor\" class=\"Hsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Lrsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Lrsfactor\" class=\"Lrsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Ssfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Ssfactor\" class=\"Ssfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Rsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Rsfactor\" class=\"Rsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Wxsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Wxsfactor\" class=\"Wxsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Wysfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Wysfactor\" class=\"Wysfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Exsfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Exsfactor\" class=\"Exsfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td><input id=\"Eysfactor'+Number($("#servicecomboTable tbody tr").length + 1).toString() +'\" name=\"Eysfactor\" class=\"Eysfactor input-sm\" style=\"width:59px\" type=\"number\" step=\"any\" value=\"0\"></td>' +
                        '<td>' +
                        '<select id=\"slspattern\" class=\"slspattern input-sm\" name=\"slspattern\" style=\"width:59px\">' +
                            '<option value=\"1\"> y </option>' +
                            '<option value=\"0\"> n </option>' +
                        '</select>' +
                        '</td>' +
                        '<td>' +    
                        '<button type=\"button\" class=\"addServiceCombo btn btn-secondary btn-success btn-sm\">' +
                        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                        '</svg>' +
                        '</button>' +
                        '<a href=\"#\" class=\"removeServiceCombo badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
                        '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
                        '</svg></a>' +
                        '</td>' +
                        '</tr>';
        
        $curRow.after($newRow);

        //expand function to renumber the remaining supports
        tableBody.children('.serviceCombo').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('S'+String(i+1));
        });
        
        UpdateChart();
    });

    // Add service combo for each button after the first one
    $("tbody").on("click", ".addServiceCombo", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        var $newRow = $curRow.clone(true);
        
        $curRow.after($newRow);
        
        //expand function to renumber the remaining supports
        tableBody.children('.serviceCombo').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text('S'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Remove a service combo
    $("tbody").on("click", ".removeServiceCombo", function(event){
        
        // prevent the vertical scroll reset
        event.preventDefault();

        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //remove the row
        $(this).closest("tr").remove();
        
        //expand function to renumber the remaining supports
        tableBody.children('.serviceCombo').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('S'+String(i+1));
        });
        
        UpdateChart();
        
    });


    // Add the 2nd distributed load
    $("tbody").on("click",".addDistLoadFirst", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");

        //new row
        var id_iterator = '_'+Number($("#distloadTable tbody tr").length + 1).toString()
        var $newRow = '<tr class=\"userDistLoad\">' +
                        '<td class=\"distloaduid\">D'+ id_iterator +'</td>' +
                        '<td><input id=\"w1'+ id_iterator +'\" name=\"w1\" class=\"w1 input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td><input id=\"trib1'+ id_iterator +'\" name=\"trib1\" class=\"trib1 input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td><input id=\"w2'+ id_iterator +'\" name=\"w2\" class=\"w2 input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td><input id=\"trib2'+ id_iterator +'\" name=\"trib2\" class=\"trib2 input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td><input id=\"dista'+ id_iterator +'\" name=\"dista\" class=\"dista input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td><input id=\"distb'+ id_iterator +'\" name=\"distb\" class=\"distb input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"1.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td>' +
                        '<select id=\"distloadType\" class=\"distloadType input-sm\" name=\"distloadType\" style=\"width:95px\" onChange=\"UpdateChart();\">' +
                        '<option value=\"D\"> D </option>' +
                        '<option value=\"F\"> F </option>' +
                        '<option value=\"L\"> L </option>' +
                        '<option value=\"H\"> H </option>' +
                        '<option value=\"Lr\"> L<sub>r</sub> </option>' +
                        '<option value=\"S\"> S </option>' +
                        '<option value=\"R\"> R </option>' +
                        '<option value=\"Wx\"> Wx </option>' +
                        '<option value=\"Wy\"> Wy </option>' +
                        '<option value=\"Ex\"> Ex </option>' +
                        '<option value=\"Ey\"> Ey </option>' +
                        '</select>' +
                        '</td>' +
                        '<td>' +    
                        '<button type=\"button\" class=\"addDistLoad btn btn-secondary btn-success btn-sm\">' +
                        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                        '</svg>' +
                        '</button>' +
                        '<a href=\"#\" class=\"removeDistLoad badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
                        '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
                        '</svg></a>' +
                        '</td>' +
                        '</tr>'
        
        $curRow.after($newRow);

        //expand function to renumber the remaining supports
        tableBody.children('.userDistLoad').each(function(i) {
            // Renumber the row
                $(this).children("td:first").text('D'+String(i+1));
            });
            
        UpdateChart();

    });

    // Add additional dist loads
    $("tbody").on("click", ".addDistLoad", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        var $newRow = $curRow.clone(true);
        
        $curRow.after($newRow);
        
        //expand function to renumber the remaining supports
        tableBody.children('.userDistLoad').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text('D'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Remove a distributed load
    $("tbody").on("click", ".removeDistLoad", function(event){
        
        // prevent the vertical scroll reset
        event.preventDefault();

        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //remove the row
        $(this).closest("tr").remove();
        
        //expand function to renumber the remaining supports
        tableBody.children('.userDistLoad').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('D'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Add the 2nd point load
    $("tbody").on("click",".addPointLoadFirst", function(){
    
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");

        //new row
        var $newRow = '<tr class=\"userPointLoad\">' +
                        '<td class=\"pointloaduid\">P'+ Number($("#pointloadTable tbody tr").length + 1).toString() +'</td>' +
                        '<td><input id=\"pointLoad'+ Number($("#pointloadTable tbody tr").length + 1).toString() +'\" name=\"pointLoad\" class=\"pointLoad input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0\" onChange=\"UpdateChart();\"></td>' +
                        '<td><input id=\"pointLoada'+ Number($("#pointloadTable tbody tr").length + 1).toString() +'\" name=\"pointLoada\" class=\"pointLoada input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td>' +
                        '<select id=\"pointloadType\" class=\"pointloadType input-sm\" name=\"pointloadType\" style=\"width:95px\" onChange=\"UpdateChart();\">' +
                        '<option value=\"D\"> D </option>' +
                        '<option value=\"F\"> F </option>' +
                        '<option value=\"L\"> L </option>' +
                        '<option value=\"H\"> H </option>' +
                        '<option value=\"Lr\"> L<sub>r</sub> </option>' +
                        '<option value=\"S\"> S </option>' +
                        '<option value=\"R\"> R </option>' +
                        '<option value=\"Wx\"> Wx </option>' +
                        '<option value=\"Wy\"> Wy </option>' +
                        '<option value=\"Ex\"> Ex </option>' +
                        '<option value=\"Ey\"> Ey </option>' +
                        '</select>' +
                        '</td>' +
                        '<td class=\"text-nowrap\">' +    
                        '<button type=\"button\" class=\"addPointLoad btn btn-secondary btn-success btn-sm\">' +
                        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                        '</svg>' +
                        '</button>' +
                        '<a href=\"#\" class=\"removePointLoad badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
                        '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
                        '</svg></a>' +
                        '</td>' +
                        '</tr>'
        
        
        $curRow.after($newRow);

        //expand function to renumber the remaining supports
        tableBody.children('.userPointLoad').each(function(i) {
            // Renumber the row
                $(this).children("td:first").text('P'+String(i+1));
            });
            
        UpdateChart();
    });

    // Add additional point loads
    $("tbody").on("click", ".addPointLoad", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        var $newRow = $curRow.clone(true);
        
        $curRow.after($newRow);
        
        //expand function to renumber the remaining supports
        tableBody.children('.userPointLoad').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text('P'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Remove a point load
    $("tbody").on("click", ".removePointLoad", function(event){
        
        // prevent the vertical scroll reset
        event.preventDefault();

        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //remove the row
        $(this).closest("tr").remove();
        
        //expand function to renumber the remaining supports
        tableBody.children('.userPointLoad').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('P'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Add 2nd moment load
    $("tbody").on("click",".addPointMomentFirst", function(){
    
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");

        //new row
        var $newRow = '<tr class=\"userPointMoment\">' +
                        '<td class=\"pointmomentuid\">M'+ Number($("#pointmomentTable tbody tr").length + 1).toString() +'</td>' +
                        '<td><input id=\"pointMoment'+ Number($("#pointmomentTable tbody tr").length + 1).toString() +'\" name=\"pointMoment\" class=\"pointMoment input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0\" onChange=\"UpdateChart();\"></td>' +
                        '<td><input id=\"pointMomenta'+ Number($("#pointmomentTable tbody tr").length + 1).toString() +'\" name=\"pointMomenta\" class=\"pointMomenta input-sm\" style=\"width:95px\" type=\"number\" step=\"any\" value=\"0.0\" onChange=\"UpdateChart();\"></td>' +
                        '<td>' +
                        '<select id=\"pointMomentType\" class=\"pointMomentType input-sm\" name=\"pointMomentType\" style=\"width:95px\" onChange=\"UpdateChart();\">' +
                        '<option value=\"D\"> D </option>' +
                        '<option value=\"F\"> F </option>' +
                        '<option value=\"L\"> L </option>' +
                        '<option value=\"H\"> H </option>' +
                        '<option value=\"Lr\"> L<sub>r</sub> </option>' +
                        '<option value=\"S\"> S </option>' +
                        '<option value=\"R\"> R </option>' +
                        '<option value=\"Wx\"> Wx </option>' +
                        '<option value=\"Wy\"> Wy </option>' +
                        '<option value=\"Ex\"> Ex </option>' +
                        '<option value=\"Ey\"> Ey </option>' +
                        '</select>' +
                        '</td>' +
                        '<td class=\"text-nowrap\">' +
                        '<button type=\"button\" class=\"addPointMoment btn btn-secondary btn-success btn-sm\">' +
                        '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-plus\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z\"/>' +
                        '</svg>' +
                        '</button>' +
                        '<a href=\"#\" class=\"removePointMoment badge badge-danger\" style=\"margin-left: 5px\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" fill=\"currentColor\" class=\"bi bi-trash\" viewBox=\"0 0 16 16\">' +
                        '<path d=\"M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z\"/>' +
                        '<path fill-rule=\"evenodd\" d=\"M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z\"/>' +
                        '</svg></a>' +
                        '</td>' +
                        '</tr>'

        $curRow.after($newRow);

        //expand function to renumber the remaining supports
        tableBody.children('.userPointMoment').each(function(i) {
            // Renumber the row
                $(this).children("td:first").text('M'+String(i+1));
            });
            
        UpdateChart();
    });

    // Add additional moment loads
    $("tbody").on("click", ".addPointMoment", function(){
        
        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //get the current row
        var $curRow = $(this).closest("tr");
        
        var $newRow = $curRow.clone(true);
        
        $curRow.after($newRow);
        
        //expand function to renumber the remaining supports
        tableBody.children('.userPointMoment').each(function(i) {
        // Renumber the row
          $(this).children("td:first").text('M'+String(i+1));
        });
        
        UpdateChart();
        
    });

    // Remove a moment load
    $("tbody").on("click", ".removePointMoment", function(event){
        
        // prevent the vertical scroll reset
        event.preventDefault();

        //get the current parent
        var tableBody = $(this).closest("tbody");
        
        //remove the row
        $(this).closest("tr").remove();
        
        //expand function to renumber the remaining supports
        tableBody.children('.userPointMoment').each(function(i) {
        // Renumber the row
            $(this).children("td:first").text('M'+String(i+1));
        });
        
        UpdateChart();
        
    });

    $(".chartUpdate").change(function(){
        UpdateChart();
    });

};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
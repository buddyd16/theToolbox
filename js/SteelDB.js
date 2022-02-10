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

    var current_shapeset;
    var previous_shapeset;

    $(function () {
        $("#shapeSet").change();
    });

    // On shape type selection update the shape list
    $("#shapeSet").on("change",function(){
        var shapeset = $('#shapeSet').find(":selected").val();
        previous_shapeset = current_shapeset
        current_shapeset = shapeset

        console.log(shapeset);
        console.log(shapeset==="WF" || shapeset==="M" || shapeset==="S" || shapeset==="HP");

        if(shapeset==="WF" || shapeset==="M" || shapeset==="S" || shapeset==="HP"){
            $("#steelFig").attr("src","static/images/steel_fig1.jpg");
            $("#steelFig").attr("width","225");
        } else if (shapeset==="C" || shapeset==="MC"){
            $("#steelFig").attr("src","static/images/steel_fig2.jpg");
            $("#steelFig").attr("width","225");
        } else if (shapeset==="L"){
            $("#steelFig").attr("src","static/images/steel_fig3.jpg");
            $("#steelFig").attr("width","315");
        } else{
            $("#steelFig").attr("src","");
        };

        $.ajax({
            url: "/steeldbapi",
            type: "GET",
            dataType: "json",
            data:{"shapeset": shapeset, "shapelist": 1},

            success: function(shapelist){

                $('#shapeList').empty();

                for (let i=0; i< shapelist.length; i++) {
                    $('#shapeList').append('<option value='+ shapelist[i] +'>'+shapelist[i]+'</option>');
                };

                //trigger a change event on the shapelist
                $("#shapeList").trigger("change");

                $("#shapeText").text("Shapes (All) :");

            },
            error: function(error){
                console.log("Error:");
                console.log(error);
            }
        });

    });

    //On shape selection get the shape properties
    $("#shapeList").on("change",function(){
        var shapeset = $('#shapeSet').find(":selected").val();
        var shape = $('#shapeList').find(":selected").val();
        var prop_highlight = $('#propertyHighlight').find(":selected").val();
        var prop_filter = $('#propertyFilter').find(":selected").val();
        var prop_filter2 = $('#propertyFilter2').find(":selected").val();

        console.log(shape);
        console.log(shape===undefined);

        $("#propselectText").text(''+shape+' -- select a property to highlight:');

        if(shape===undefined){
            // clear out the output table and highlight options
            $('#shapeProperties').empty();
            $('#propertyHighlight').empty();
            $('#propertyFilter').empty();
            $('#propertyFilter2').empty();

        } else{
            $.ajax({
                url: "/steeldbapi",
                type: "GET",
                dataType: "json",
                data:{"shapeset": shapeset, "shape": shape},

                success: function(shapedata){

                    // clear out the output table and highlight options
                    $('#shapeProperties').empty();
                    $('#propertyHighlight').empty();
                    $('#propertyFilter').empty();
                    $('#propertyFilter2').empty();

                    Object.keys(shapedata).forEach(function(key){

                        if (shapedata[key][0]!=='0.0000' && key!=='Type'){
                            let str = '<tr id="'+key+'" class=""><td id="'+key+'" class="text-right text-nowrap">'+key+'</td><td class="text-center text-nowrap">'+shapedata[key][0]+'</td><td class="text-center text-nowrap">'+shapedata[key][1]+'</td><td>'+shapedata[key][2]+'</td></tr>';
                            $('#shapeProperties').append(str);
                            $('#propertyHighlight').append('<option value='+ key +'>'+key+'</option>');

                            if(key!=='EDI_Std_Nomenclature' && key!=='AISC_Manual_Label' && key!=='T_F'){
                                $('#propertyFilter').append('<option value='+ key +'>'+key+'</option>');
                                $('#propertyFilter2').append('<option value='+ key +'>'+key+'</option>');
                            };
                        };
                    });
                    
                    //if the shape set didn't change reset the filter property to the one previously selected
                    $('#propertyHighlight').val(prop_highlight).prop('selected', true);
                    $('#propertyFilter').val(prop_filter).prop('selected', true);
                    $('#propertyFilter2').val(prop_filter2).prop('selected', true);

                    
                    //trigger change event on the highlightProperty list
                    $("#propertyHighlight").change();

                },
                error: function(error){
                    console.log("Error:");
                    console.log(error);
                }
            });
        };

    });

    //On property highlight select change table row class to bootstrap success
    $("#propertyHighlight").on("change",function(){

        var prop = $('#propertyHighlight').find(":selected").val();

        // clear out the output table
        $('#selectPropTable').empty();

        //Loop through the property table and read the row id
        //set the highlight if the id matches the selected prop
        $('#shapeProperties tr').each(function(){
            
            var cur_id =  $(this).attr('id');
            var curclone = $(this).clone()
            curclone.addClass("bg-success");

            if (cur_id === prop){
                $(this).addClass("bg-success");
                $('#selectPropTable').append(curclone);
            }  else{
                $(this).removeClass("bg-success");
            };
        });

    });

    //Button to filter the Shape List
    $('#buttonshapeFilter').button().click(function(){
        var shapeset = $('#shapeSet').find(":selected").val();
        var filter_prop = $('#propertyFilter').find(":selected").val();
        var filter_start = $('#propertyfilterstartValue').val();
        var filter_end = $('#propertyfilterendValue').val();

        $.ajax({
            url: "/steeldbapi",
            type: "GET",
            dataType: "json",
            data:{"shapeset": shapeset, "shapelist": 1, "shapefilterprop": filter_prop, "shapefilterstart": filter_start, "shapefilterend": filter_end},

            success: function(shapelist){
                $('#shapeList').empty();

                for (let i=0; i< shapelist.length; i++) {
                    $('#shapeList').append('<option value='+ shapelist[i] +'>'+shapelist[i]+'</option>');
                };

                //trigger a change event on the shapelist
                $("#shapeList").trigger("change");

                //Indicate the shape list was filtered
                $("#shapeText").html("Shapes (Filtered) :<br>"+filter_start+" &#8804; "+ filter_prop +" &#8804; "+filter_end+"");
            },
            error: function(error){
                console.log("Error:");
                console.log(error);
            }
        });

    });

    //Button to filter the Shape List by both filters
    $('#buttonshapeFilter2').button().click(function(){
        var shapeset = $('#shapeSet').find(":selected").val();
        var filter_prop = $('#propertyFilter').find(":selected").val();
        var filter_start = $('#propertyfilterstartValue').val();
        var filter_end = $('#propertyfilterendValue').val();
        var filter_prop2 = $('#propertyFilter2').find(":selected").val();
        var filter_start2 = $('#propertyfilterstartValue2').val();
        var filter_end2 = $('#propertyfilterendValue2').val();

        $.ajax({
            url: "/steeldbapi",
            type: "GET",
            dataType: "json",
            data:{"shapeset": shapeset, "shapelist": 1, "shapefilterprop": filter_prop, "shapefilterstart": filter_start, "shapefilterend": filter_end, "shapefilterprop2": filter_prop2, "shapefilterstart2": filter_start2, "shapefilterend2": filter_end2},

            success: function(shapelist){
                $('#shapeList').empty();

                for (let i=0; i< shapelist.length; i++) {
                    $('#shapeList').append('<option value='+ shapelist[i] +'>'+shapelist[i]+'</option>');
                };

                //trigger a change event on the shapelist
                $("#shapeList").trigger("change");

                //Indicate the shape list was filtered
                $("#shapeText").html("Shapes (Filtered) :<br>"+filter_start+" &#8804; "+ filter_prop +" &#8804; "+filter_end+"<br>"+filter_start2+" &#8804; "+ filter_prop2 +" &#8804; "+filter_end2+"");
            },
            error: function(error){
                console.log("Error:");
                console.log(error);
            }
        });

    });
    //Button to Reset the Shape List
    $('#buttonshapeReset').button().click(function(){
        $("#shapeSet").change();
        $("#shapeText").text("Shapes (All) :");
    });
};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
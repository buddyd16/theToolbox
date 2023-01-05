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

//Function to update the Species selection
function updateSpecies(stud){

  var ndsTable = 0;
  var ndsSelect = 0;

  if (stud){
    ndsTable = $('#nds_supp_table_select').find(":selected").val();
    ndsSelect = '#nds_species_select';
  } else {
    ndsTable = $('#nds_supp_table_select_plate').find(":selected").val();
    ndsSelect = '#nds_species_select_plate';
  }

  if (ndsTable == 0){
    return 1;
  } else if (ndsTable == "USER"){
    if (stud){
      $('.stud_ref_values').prop("readonly",false);
      $('#nds_grade_select').empty();
      $('#nds_grade_select').append('<option value=\"USER\"> USER </option>');
    } else {
      $('.plate_ref_values').prop("readonly",false);
      $('#nds_grade_select_plate').empty();
      $('#nds_grade_select_plate').append('<option value=\"USER\"> USER </option>');
    }

    $(ndsSelect).empty();
    $(ndsSelect).append('<option value=\"USER\"> USER </option>');

  } else {

    if (stud){
      $('.stud_ref_values').prop("readonly",true);
    } else {
      $('.plate_ref_values').prop("readonly",true);
    }

    $.ajax({
      url: "/wood/ndsdb_api",
      type: "GET",
      dataType: "json",
      data:{"table": ndsTable, "keys": true},

      success: function(ndsSpecies){

          $(ndsSelect).empty();

          for (let i=0; i< ndsSpecies.length; i++) {
              $(ndsSelect).append('<option value='+ ndsSpecies[i].replaceAll(' ','_') +'>'+ndsSpecies[i]+'</option>');
          };

          //trigger a change event on the shapelist
          $(ndsSelect).trigger("change");

          return 0;
      },
      error: function(error){
          console.log("Error:");
          console.log(error);
          return 2;
      }
    });
  }
};

// Function to update the grade select lists
function updateGrades(stud){
  console.log(stud);
  var ndsTable = 0
  var ndsSpecies = 0
  var shapeD = $('#stud_d').find(":selected").val();
  var ndsGradeSelect = 0;

  if (stud == true){
    ndsTable = $('#nds_supp_table_select').find(":selected").val();
  } else {
    ndsTable = $('#nds_supp_table_select_plate').find(":selected").val();
  }

  console.log(ndsTable);

  if (ndsTable == "USER"){
    console.log(ndsTable);
    return 0;
  } else {
    if (stud == true){
      ndsSpecies = $('#nds_species_select').find(":selected").val().replaceAll('_',' ');
      ndsGradeSelect = '#nds_grade_select';
    } else {
      ndsSpecies = $('#nds_species_select_plate').find(":selected").val().replaceAll('_',' ');
      ndsGradeSelect = '#nds_grade_select_plate';
    }

    console.log(ndsTable);

    if (ndsTable == 0 && ndsSpecies == 0){
      return 1;
    } else {
      $.ajax({
        url: "/wood/ndsdb_api",
        type: "GET",
        dataType: "json",
        data:{"table": ndsTable, "keys": true, "species": ndsSpecies, "depth":shapeD},

        success: function(ndsGrade){

            $(ndsGradeSelect).empty();
            console.log(ndsGrade);

            for (let i=0; i< ndsGrade.length; i++) {
                $(ndsGradeSelect).append('<option value='+ ndsGrade[i].replaceAll(' ','_') +'>'+ndsGrade[i]+'</option>');
            };

            //trigger a change event on the grade list
            $(ndsGradeSelect).trigger("change");
            return 0;
        },
        error: function(error){
            console.log("Error:");
            console.log(error);
            return 2;
        }
      });
    }
  }
};


// function to update reference values
function updateReferenceValues(stud){
  var ndsTable = 0
  var ndsSpecies = 0
  var ndsGrade = 0
  var shapeD = $('#stud_d').find(":selected").val();

  if (stud == true){
    var ndsTable = $('#nds_supp_table_select').find(":selected").val();
    var ndsSpecies = $('#nds_species_select').find(":selected").val().replaceAll('_',' ');
    var ndsGrade = $('#nds_grade_select').find(":selected").val().replaceAll('_',' ');
  }else{
    var ndsTable = $('#nds_supp_table_select_plate').find(":selected").val();
    var ndsSpecies = $('#nds_species_select_plate').find(":selected").val().replaceAll('_',' ');
    var ndsGrade = $('#nds_grade_select_plate').find(":selected").val().replaceAll('_',' ');
  }

  if (ndsTable==0 || ndsSpecies == 0 || ndsGrade == 0 ){
    return 1;
  } else {
    $.ajax({
      url: "/wood/ndsdb_api",
      type: "GET",
      dataType: "json",
      data:{"table": ndsTable, "grade": ndsGrade, "species": ndsSpecies, "depth":shapeD},

      success: function(ndsRefValues){

          console.log(ndsRefValues);
          if (stud ==  true){
            $('#fb_input').val(ndsRefValues['Reference Values']['Fb']);
            $('#ft_input').val(ndsRefValues['Reference Values']['Ft']);
            $('#fv_input').val(ndsRefValues['Reference Values']['Fv']);
            $('#fcp_input').val(ndsRefValues['Reference Values']['Fcp']);
            $('#fc_input').val(ndsRefValues['Reference Values']['Fc']);
            $('#E_input').val(ndsRefValues['Reference Values']['E']);
            $('#Emin_input').val(ndsRefValues['Reference Values']['Emin']);
            $('#G_input').val(ndsRefValues['Reference Values']['G']);
            $('#agency_input').val(ndsRefValues['Agency']);
          } else {
            $('#fb_input_plate').val(ndsRefValues['Reference Values']['Fb']);
            $('#ft_input_plate').val(ndsRefValues['Reference Values']['Ft']);
            $('#fv_input_plate').val(ndsRefValues['Reference Values']['Fv']);
            $('#fcp_input_plate').val(ndsRefValues['Reference Values']['Fcp']);
            $('#fc_input_plate').val(ndsRefValues['Reference Values']['Fc']);
            $('#E_input_plate').val(ndsRefValues['Reference Values']['E']);
            $('#Emin_input_plate').val(ndsRefValues['Reference Values']['Emin']);
            $('#G_input_plate').val(ndsRefValues['Reference Values']['G']);
            $('#agency_input_plate').val(ndsRefValues['Agency']);
          }

          return 0;
      },
      error: function(error){
          console.log("Error:");
          console.log(error);
          return 2;
      }
    });
  }
};

// This function is used for event handlers after the HTML document loads
function main() {

    // trigger initial on change actions
    $(function () {
      $("#stud_b").change();
      //$("#nds_supp_table_select").change();
      //$("#nds_supp_table_select_plate").change();
    });

    $("#stud_b,#stud_d,#stud_plys").on("change",function(){
        
        let b_nom = $('#stud_b').find(":selected").val();
        let d_nom = $('#stud_d').find(":selected").val();
        let num_plys = Number($('#stud_plys').find(":selected").val());
        let actual_dims = nds_actual_dimensions(b_nom,d_nom,num_plys);

        $('#actual_stud_dims').html(''+actual_dims[0].toFixed(2).toString()+' in. x '+actual_dims[1].toFixed(2).toString()+' in.');

    });

    // When depth changes fire the change events for grade selections
    // so that proper grades show
    $("#stud_d").on("change",function(){
      $('#nds_species_select').trigger("change");
      $('#nds_species_select_plate').trigger("change");

      // Alert user that grade selection needs to be done again
      alert("Changing Depth requires reselecting material grade as they vary with depth.");
    });

    // On Supplement Table Selection update the Species selection
    $("#nds_supp_table_select").on("change",function(){
      
      updateSpecies(true);

    });

    $("#nds_supp_table_select_plate").on("change",function(){
      
      updateSpecies(false);

    });

    // On Species Change update the grades
    $("#nds_species_select").on("change",function(){

      updateGrades(true);

    });

    $("#nds_species_select_plate").on("change",function(){

      updateGrades(false);

    });

    // On Grade Change update the reference values
    $("#nds_grade_select").on("change",function(){

      updateReferenceValues(true);

    });

    $("#nds_grade_select_plate").on("change",function(){

      updateReferenceValues(false);

    });

};

// Ensure the full HTML document loads before running any functions
$(document).ready(main);
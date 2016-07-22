//local version
var warn_on_unload = "You have unsaved changes!"

jQuery(document).ready(function($) {

  var BrtMorphologyDict = $("#BrtMorphologyDict").val();                                 // data for
  var BrtMorphologyClassArray = JSON.parse(BrtMorphologyDict);                           // Morphology select
  var GynMorphologyDict = $("#GynMorphologyDict").val();
  var GynMorphologyClassArray = JSON.parse(GynMorphologyDict);
  var mvSpeed=1000                                                                       // page slider speed
  var mvSpeedF=500
  if (navigator.userAgent.search("MSIE") >= 0) {var browser='IE'} else {var browser=''}; // get browser type
  var currPg='1';                                                                        // set 'current' page flag
  var newPg='1';

  if ($.session.get('Pgvalue')!=undefined) {                                             // get/set current page
    currPg=$.session.get('Pgvalue');
  }
  else {
    $.session.set('Pgvalue', '1');
    currPg='1';
  }
  // some code changes made here in test-branch2
  // -- new specimen --------------------------------------------------------------------------------------------------
  elSID=$('#id_clinical_sample_id');
  SID=elSID.val();
  if (SID!='') {                                                                         // if we have a SID
    elSID.attr('readonly',true);                                                         //  set it to read only
    }
  else {
    $(".pidhdr").text('');                                                               // else display dialog
    $(".web_dialog").css({"display":"block"});                                           //  to add new SID
    $('.submit1').css({'display':'none'});                                               //  and hide submit
    $("#GEL_header").text('GELCI - Add sample');                                         //  modify header
  }
  // -- /new specimen -------------------------------------------------------------------------------------------------

  // -- web_dialog (add new specimen) ---------------------------------------------------------------------------------
  $("#AddSampleHdr").css({"font-weight":"bold","width":"100px","position":"absolute","left":"10px","top":"10px"});
  $("#div_id_new_clinical_sample_id").css({"width":"30px","height":"27px","position":"absolute","left":"40px","top":"100px"});
  $("#id_new_clinical_sample_id").css({"border":"1px solid #336699","width":"20px"});
  $("#div_id_pid_select").css({"position":"absolute","left":"40px","top":"40px"});
  $("#id_pid_select").css({"border":"1px solid #336699"});
  $("#div_go_button").css({"position":"absolute","left":"240px","top":"170px"});
  $("#id_new_clinical_sample_id").val("1").prop("readonly", true);
  // build PID select element
  var URL="/PIDlist/";
  $.ajax({                                                                               // get participant list
    cache: false,
    type: "GET",
    url: URL,
    async: false,
    dataType: "json",
    success: function(data){
      for (var i=0;i<data.length;i++){                                                   // add options to select
        var opt=$('<option/>').val(data[i][0]).html(data[i][1])
        opt.appendTo('#id_pid_select');
        if (data[i][2]=='linked') {opt.prop('disabled', true);}                          // disable opt if PID already
        else {
          //opt.css({"font-weight":"bold"});  // bold not working in IE
          opt.css({'color':'seagreen'});

          }                                          // has a linked SID
      }
      $("#id_pid_select").prepend("<option value='' selected='selected'></option>");     // default to blank option
    }
  });
  // 'go' button action
  $("#div_go_button").click(function(){
    PID=$("#id_pid_select").val();
    SID=$("#id_pid_select").val()+'_'+$("#id_new_clinical_sample_id").val();             // initial ID -
    if (SID==''||PID=='') {                                                              // need to do dev for _2,_3 etc
      //alert('Sample ID and Participant ID must be entered')
      $("#id_new_clinical_sample_id").focus();
    }
    else {
      var x=AddSpecimenRecord(SID,PID,function() {
        $(window).off('beforeunload');                                                   // see window.bind funct below
        window.location.href='/specimen/add/'+PID+'/'+SID+'/' ;                          // lnk to views.get_SpecimenAdd
      });
      if (containsString(x, 'fail')) {
      }
    }
  })
  // -- /web_dialog ---------------------------------------------------------------------------------------------------

  // -- form layout ---------------------------------------------------------------------------------------------------
  // page element layout
  var layoutDict = $("#layoutDict").val();                                               // layout values are stored
  var layoutClassArray = JSON.parse(layoutDict);                                         // on geldbx_layout table
  $.each(layoutClassArray, function( el, Values ) {                                      // for each element
    $("#div_id_"+el).addClass(Values[0]);                                                //  add row/col classes
    $("#id_"+el).css({"background-color":Values[1]});                                    //  set background colour
    $("#id_"+el).addClass(Values[2]);                                                    //  add additional classes
  })
  // set page element layout row offset for .rfN
  var foff=40;                                                                           // initial offset for rows
  for(var row = 1; row <=19; row++) {                                                    // set row offset
    var offset=50*(row-1)+foff;
    $(".rf"+row).css({"position":"absolute","top":offset+ "px"})
  }
  // set tab indices
  var cols = ['.cf1','.cf2a','.cf4'];
  DoTabIndexPg('.Pg1',cols,'.rf',1,5);
  var cols = ['.cf1','.cf2','.cf4'];
  DoTabIndexPg('.Pg2',cols,'.rf',2,9);
  var cols = ['.cf1','.cf2b','.cf3a','.cf4a'];
  DoTabIndexPg('.Pg3',cols,'.rf',1,13);

  $('.ffdna, .ffpedna, .blood').each(function() {
    var elid = $(this).attr('id')
    if (elid.indexOf('dtm')>=0) {
      $('label[for="'+elid+'"]').css({'text-align':'right','width':'115px'})
    }
  })

  $('.numberinput.ffdna, .numberinput.ffpedna, .numberinput.blood').css({'width':'60px'})
  // -- /form layout --------------------------------------------------------------------------------------------------

  // -- initialisation ------------------------------------------------------------------------------------------------
  $('#div_id_xml_status').css({'display':'none'});
  // default values
  //if ($("#id_blood_dna_extraction_method").val()==""){$("#id_blood_dna_extraction_method").val($("#metadata").attr('BLOOD_DNA_EXT_METH'))}; removed for v2 21/1/15
  //if ($("#id_ff_dna_extraction_method").val()=="") {$("#id_ff_dna_extraction_method").val($("#metadata").attr('FF_DNA_EXT_METH'))};
  //if ($("#id_ffpe_dna_extraction_method").val()=="") {$("#id_ffpe_dna_extraction_method").val($("#metadata").attr('FFPE_DNA_EXT_METH'))};
  if ($("#id_ffpe_fixative_type").val()=="") {$("#id_ffpe_fixative_type").val($("#metadata").attr('FFPE_FIX_TYPE'))};
  if ($("#id_gmc_clinic_id").val()=="") {$("#id_gmc_clinic_id").val($("#metadata").attr('GMC_CLINIC_ID'))};
  if ($("#id_gmc_lab_id").val()=="") {$("#id_gmc_lab_id").val($("#metadata").attr('GMC_LAB_ID'))};
  if ($("#id_gmc_tissue_lab_id").val()=="") {$("#id_gmc_tissue_lab_id").val($("#metadata").attr('GMC_TISSUE_LAB_ID'))};
  if ($("#id_haem_malignancy").val()=="") {$("#id_haem_malignancy").val('N')};
  // remove blank option for haem malignancy, constitutional tissue, formalin fixed used
  $('.noblank').each(function() {$('option[value=""]', this).remove();});
  // hide unused elements
  $("#div_id_clinical_sample_id, #div_id_microdissection_used, #div_id_microdissection_details, #div_id_ffpe_slide_marked_by, #div_id_ffpe_slide_marked_date").addClass("unused");
  $("#div_id_ff_snap_freezing_end_dtms, #div_id_ff_section_cut_by, #div_id_ff_section_cut_date, #div_id_ff_section_assessed_by, #div_id_ff_section_assessed_date").addClass("unused");
  $("#div_id_pathology_comments, #div_id_blood_dna_extraction_method").addClass("unused");
  $("#div_id_blood_dna_sample_rack_well,#div_id_ffpe_dna_sample_rack_well,#div_id_ff_dna_sample_rack_well").children().hide();
  $(".unused").addClass("hidden");
  // tweak widths/positions
  $("#id_ffpe_time_in_formalin").css({'width':'50px'});
  $("#id_ff_dna_extraction_method, #id_ffpe_dna_extraction_method, #id_lab_sample_not_sent_reason").css({'width':'220px'});
  $("#id_ffpe_fixative_type, #id_ffpe_fixation_comments, #id_ffpe_slide_marked_by, #id_microdissection_details,"+
    "#id_macrodissection_details").css({'width':'300px'});
  $("#id_pathology_comments,#id_excision_margin,#id_non_invasive_elements,#id_morphology").css({'width':'380px'});
  $(".samplesubmit").css({'top':'660px'});
  // unused select options - include for legacy purposes - but disable further selection
  greyout("#id_ffpe_dna_extraction_method > option", 'CMDL_LP_020_DNA v1.0')
  greyout("#id_ff_dna_extraction_method > option", 'CMDL_LP_003_DNA v1.0')
  greyout("#id_ffpe_processing_schedule > option", 'Rapid run*Extra large program')
  greyout("#id_blood_dna_lab_method > option", 'Gel_SOP469 v1.0')
    // -- clear/disable biopsy guage/count if tissue source is resection
  $('.biopsy').each(function() {$('#div_'+$(this).attr('id')).addClass('biopsygroup')});
  if ($("#id_sample_provenance").val()=='surgical resection') {
    $(".biopsy").val('').prop('disabled', true);
    $('.biopsygroup').css({'color':'gray'});
  };
  // date/time picker setup
  //$('input[id$="_dtm"], #id_lab_sample_sent_date').datetimepicker({dateFormat: "dd/mm/yy",stepMinute:"1",timeFormat:"hh:mm",showOn:"button",buttonImage:"/static/datepicker.gif"});
/*
  $('input[id$="_dtm"]').datetimepicker({dateFormat: "dd/mm/yy",stepMinute:"1",timeFormat:"hh:mm",showOn:"button",buttonImage:"/static/datepicker.gif"});
  $('#id_lab_sample_sent_date').datetimepicker({dateFormat: "dd/mm/yy",stepMinute:"1",timeFormat:"hh:mm",showOn:"button",buttonImage:"/static/datepicker.gif"});
  $('input[id*="_date"]').not('#id_lab_sample_sent_date').datepicker({dateFormat:'dd/mm/yy',showOn:"button",buttonImage:"/static/datepicker.gif" });
  $('input[id$="_dtms"]').datetimepicker({dateFormat: "dd/mm/yy",stepMinute:"1",showSecond: true,stepSecond:"1", timeFormat:"hh:mm:ss",showOn:"button",buttonImage:"/static/datepicker.gif"});
  $('input[id$="_dtms"]').addClass('datetimeinputsecs');
*/





  $('input[id$="_dtm"]').datetimepicker({dateFormat: "dd/mm/yy",stepMinute:"1",timeFormat:"hh:mm",showOn:"button",buttonImage:"/static/datepicker.gif"});
  //$('#id_lab_sample_sent_date').datetimepicker({dateFormat: "dd/mm/yy",stepMinute:"1",timeFormat:"hh:mm",showOn:"button",buttonImage:"/static/datepicker.gif"});
  $('input[id*="_date"]').datepicker({dateFormat:'dd/mm/yy',showOn:"button",buttonImage:"/static/datepicker.gif" });
  $('input[id$="_dtms"]').datetimepicker({dateFormat: "dd/mm/yy",stepMinute:"1",showSecond: true,stepSecond:"1", timeFormat:"hh:mm:ss",showOn:"button",buttonImage:"/static/datepicker.gif"});
  $('input[id$="_dtms"]').addClass('datetimeinputsecs');











  // time only field
  $('#id_ffpe_time_in_formalin').datetimepicker({timeInput: true, timeFormat: "hh:mm tt", timeOnly: true});
  $('#id_ffpe_time_in_formalin').mask('99:99');

  /*
  $('#id_ffpe_time_in_formalin').blur(function() {
    $('#id_ffpe_time_in_formalin').css({'border':'none'});                       // el may have border
    validate($(this), 'hhmm');                                                        // from pg submit - remove
  });
 */


  // adjust morphology select options based on topography value
  if ($("#id_topography").val()=='T87000') {
      $.each(BrtMorphologyClassArray, function( item, text ) {$("#id_morphology option[value='"+item+"']").remove();});
  }
  else {
      $.each(GynMorphologyClassArray, function( item, text ) {$("#id_morphology option[value='"+item+"']").remove();});
  }
  // turn off 'submit on enter' key press
  NoSubmitOnEnter();
  $('#LabIds').html('Blood DNA lab ID: '+$('#metadata').attr('GMC_LAB_ID')+'     Tissue DNA lab ID: '+$('#metadata').attr('GMC_TISSUE_LAB_ID'));
  // -- /initialisation -----------------------------------------------------------------------------------------------------------

  // -- ff and ffpe initialisation ------------------------------------------------------------------------------------------------
  // initial 'Fresh frozen used'  settings
  $('.ff').each(function() {$('#div_'+$(this).attr('id')).addClass('ffgroup')});         // add ffgroup class to ff
  $('.ffdna').each(function() {$('#div_'+$(this).attr('id')).addClass('ffdnagroup')});   // add ffdnagroup class to ffdna
  $('.sample').each(function() {$('#div_'+$(this).attr('id')).addClass('samplegroup')}); // add samplegroup class to sample

  $('.ff.hasDatepicker').each(function() {                                               // add ff_datapicker class to
    $(this).siblings('.ui-datepicker-trigger').addClass('ff_datepicker');                // ff datepicker elements
  })
  $('.ffdna.hasDatepicker').each(function() {                                            // ditto for ffdna
    $(this).siblings('.ui-datepicker-trigger').addClass('ffdna_datepicker');
  })
  $('.sample.hasDatepicker').each(function() {                                           // ditto for ffdna
    $(this).siblings('.ui-datepicker-trigger').addClass('sample_datepicker');
  })
  if ($("#id_ff_used").val()=='N') {                                                     // if 'Fresh frozen' selector set to 'N'
    // v3 $('.ff, .ffdna').val('');                                                            //   clear ff and ffdna element data
    $('.ff, .ffdna').prop('disabled', true);
    $('.ffgroup, .ffdnagroup').css({'color':'gray'});
    $('.ff_datepicker, .ffdna_datepicker').css({'display':'none'});
    $('#id_ff_dna_used').val('N').prop('disabled', true);                                //   and 'DNA used' selector
  }
  if ($("#id_ff_dna_used").val()=='N') {                                                 // if 'DNA selector' set to 'N'
    // v3 $('.ffdna').val('');                                                                 //     clear  ffDNA element data
    $('.ffdna').prop('disabled', true);                                                  //     and disable
    $('.ffdnagroup').css({'color':'gray'});
    $('.ffdna_datepicker').css({'display':'none'});
  };
  // initial 'Formalin fixed used' settings
  $('.ffpe').each(function() {$('#div_'+$(this).attr('id')).addClass('ffpegroup')});
  $('.ffpedna').each(function() {$('#div_'+$(this).attr('id')).addClass('ffpednagroup')});

  $('.ffpe.hasDatepicker').each(function() {
    $(this).siblings('.ui-datepicker-trigger').addClass('ffpe_datepicker');
  });
  $('.ffpedna.hasDatepicker').each(function() {
    $(this).siblings('.ui-datepicker-trigger').addClass('ffpedna_datepicker');
  });
  if ($("#id_ffpe_used").val()=='N') {                                                   // if 'Formalin fixed' selector set to 'N'
   // v3  $('.ffpe, .ffpedna').val('');                                                        //   clear ffpe and ffpedna element data
    $('.ffpe, .ffpedna').prop('disabled', true);                                         //   and disable
    $('.ffpegroup, .ffpednagroup').css({'color':'gray'});
    $('.ffpe_datepicker, .ffpedna_datepicker').css({'display':'none'});
    $('#id_ffpe_dna_used').val('N').prop('disabled', true);                              //   and 'DNA used' selector
  };
  if ($("#id_ffpe_dna_used").val()=='N') {                                               // if 'DNA selector' set to 'N'
    // v3 $('.ffpedna').val('');                                                               //     clear  ffpeDNA element data
    $('.ffpedna').prop('disabled', true);                                                //     and disable
    $('.ffpednagroup').css({'color':'gray'});
    $('.ffpedna_datepicker').css({'display':'none'});
  };
  // -- /ff and ffpe initialisation -----------------------------------------------------------------------------------------------

  // -- change of 'Fresh frozen' or 'Fresh frozen DNA used' values ----------------------------------------------------------------
    $("#id_ff_used").change(function() {                                                 // on cx 'Formalin fixed used' value
                                                                                         //
    if ($(this).val()=='Y'){                                                             // if value = 'yes'
      $('.ff').prop('disabled', false);                                                //   enable ff elements
      $('.ffgroup').css({'color':'#000080'});
      $('.ff_datepicker').css({'display':'block'});
      $('#id_ff_dna_used').prop('disabled', false);                                    //   and 'DNA used' selector
      if ($('#id_ff_dna_used').val()=='Y') {                                           //   if 'DNA used' selector = 'yes'
        $('.ffdna').prop('disabled', false);                                           //     enable ffDNA elements
        $('.ffdnagroup').css({'color':'#000080'});
        $('.ffdna_datepicker').css({'display':'block'});
      }
      else {                                                                             //   else
        $('.ffdna').prop('disabled', true);                                            //     disable ffDNA elements
        $('.ffdna_datepicker').css({'display':'none'});
      }
    }
    else {                                                                               // else
      // v3 $('.ff, .ffdna').val('');                                                      //   clear ff, ffDNA element data
      $('.ff, .ffdna').prop('disabled', true);                                       //   and disable
      $('#el_ff_rwell_A').prop("disabled", true).val('-');
      $('#el_ff_rwell_N').prop("disabled", true).val('--');
      $('.ff_datepicker').css({'display':'none'});
      $('.ffgroup, .ffdnagroup').css({'color':'gray'});
      $('.ff_datepicker, .ffdna_datepicker').css({'display':'none'});
      $('#id_ff_dna_used').val('N');
      $('#id_ff_dna_used').prop('disabled', true);                                     //   and and 'DNS used' selector
    }
  });

  $("#id_ff_dna_used").change(function() {                                             // on cx 'Formalin fixed DNA used' value
    if ($(this).val()=='N'){                                                           //   if value = 'no'
      // v3 $('.ffdna').val('');                                                             //     clear  ffDNA element data
      $('.ffdna').prop('disabled', true);                                              //     and disable
      $('#el_ff_rwell_A').prop("disabled", true).val('-');
      $('#el_ff_rwell_N').prop("disabled", true).val('--');
      $('.ffdnagroup').css({'color':'gray'});
      $('.ffdna_datepicker').css({'display':'none'});
    }
    else {                                                                               //   else
      $('.ffdna').prop('disabled', false);                                             //     enable ffDNA elements
      $('#el_ff_rwell_A').prop("disabled", false);
      $('#el_ff_rwell_N').prop("disabled", false);
      $('.ffdnagroup').css({'color':'#000080'});
      $('.ffdna_datepicker').css({'display':'block'});
    }
  });

  // -- change of 'Formalin fixed used' or 'Formalin fixed DNA used' values -----------------------------------------------------
  $("#id_ffpe_used").change(function() {                                                 // on cx 'Formalin fixed used' value
                                                                                         //
    if ($(this).val()=='Y'){                                                             // if value = 'yes'
      $('.ffpe').prop('disabled', false);                                                //   enable ffpe elements
      $('.ffpegroup').css({'color':'#000080'});
      $('.ffpe_datepicker').css({'display':'block'});
      $('#id_ffpe_dna_used').prop('disabled', false);                                    //   and 'DNA used' selector
      if ($('#id_ffpe_dna_used').val()=='Y') {                                           //   if 'DNA used' selector = 'yes'
        $('.ffpedna').prop('disabled', false);                                           //     enable ffpeDNA elements
        $('.ffpednagroup').css({'color':'#000080'});
        $('.ffpedna_datepicker').css({'display':'block'});
      }
      else {                                                                             //   else
        $('.ffpedna').prop('disabled', true);                                            //     disable ffpeDNA elements
        $('#el_ffpe_rwell_A').prop("disabled", true).val('-');
        $('#el_ffpe_rwell_N').prop("disabled", true).val('--');
        $('.ffpedna_datepicker').css({'display':'none'});
      }
    }
    else {                                                                               // else
      // v3 $('.ffpe, .ffpedna').val('');                                                      //   clear ffpe, ffpeDNA element data
      $('.ffpe, .ffpedna').prop('disabled', true);                                       //   and disable
      $('#el_ffpe_rwell_A').prop("disabled", true).val('-');
      $('#el_ffpe_rwell_N').prop("disabled", true).val('--');
      $('.ffpe_datepicker').css({'display':'none'});
      $('.ffpegroup, .ffpednagroup').css({'color':'gray'});
      $('.ffpe_datepicker, .ffpedna_datepicker').css({'display':'none'});
      $('#id_ffpe_dna_used').val('N');
      $('#id_ffpe_dna_used').prop('disabled', true);                                     //   and and 'DNS used' selector
    }
  });

  $("#id_ffpe_dna_used").change(function() {                                             // on cx 'Formalin fixed DNA used' value
    if ($(this).val()=='N'){                                                             //   if value = 'no'
      // v3 $('.ffpedna').val('');                                                             //     clear  ffpeDNA element data
      $('#el_ffpe_rwell_A').val('-');
      $('#el_ffpe_rwell_N').val('--');
      $('#el_ffpe_rwell_A').prop("disabled", true);
      $('#el_ffpe_rwell_N').prop("disabled", true);
      $('.ffpedna').prop('disabled', true);                                              //     and disable
      $('.ffpednagroup').css({'color':'gray'});
      $('.ffpedna_datepicker').css({'display':'none'});
    }
    else {                                                                               //   else
      $('.ffpedna').prop('disabled', false);                                             //     enable ffpeDNA elements
      $('#el_ffpe_rwell_A').prop("disabled", false);
      $('#el_ffpe_rwell_N').prop("disabled", false);
      $('.ffpednagroup').css({'color':'#000080'});
      $('.ffpedna_datepicker').css({'display':'block'});
    }
  });
  // -- /change of 'Formalin fixed used' or 'Formalin fixed DNA used' values ----------------------------------------------------

  // -- reload morphology select on change of Topography value ------------------------------------------------------------------
  $("#id_topography").change(function() {
    var el=$("#id_morphology");
    var currval=el.val();
    el.find('option').remove();

    if ($(this).val()=='T87000') {
      $.each(GynMorphologyClassArray, function( item, text ) {$('<option />', {value: item, text: text}).appendTo(el);});
    }
    else if ($(this).val()!='') {
      $.each(BrtMorphologyClassArray, function( item, text ) {$('<option />', {value: item, text: text}).appendTo(el);});
    };
    $("#id_morphology").prepend("<option value=''>----</option>");

    $("#id_morphology").val(currval);
  });
  // -- /reload morphology select on change of Topography value -----------------------------------------------------------------

  // -- clear/disable biopsy guage/count if tissue source is 'resection' - enable otherwise
  $("#id_sample_provenance").change(function() {
    if ($(this).val()=='surgical resection') {
      $(".biopsy").val('').prop('disabled', true);
      $('.biopsygroup').css({'color':'gray'});
    }
    else {
      $(".biopsy").prop('disabled', false);
      $('.biopsygroup').css({'color':'#000080'});
    }
  });

  // -- rack well input: create selectors and validate --------------------------------------------------------------------------
  // set select data items
  var Adata = {'':'-','A':'A','B':'B','C':'C','D':'D','E':'E','F':'F','G':'G','H':'H'};  // alpha data array
  var Ndata = {};
  for(var i=1; i <= 12; i++) {Ndata[i]=pad(i.toString(),2)}                              // numeric data array
  // create blood, ff, and ffpe rack well select elements and append respective divs
  $.each(['blood','ff','ffpe'], function(index, rw_type) {                               // for each of 'blood','ff','ffpe'
    var el=$('<select style="background-color:#a8c8b0" class="rwselect" name="DNA sample rack well" />');
    var div_id=rw_type+'_rwell';
    var labeltxt=(rw_type=='blood')?'Blood DNA sample rack well':rw_type.toUpperCase()+' DNA sample rack well';
    for(var val in Adata) {$('<option />', {value: val, text: Adata[val]}).appendTo(el);}// create an alpha select element
    el.attr('id','el_'+div_id+'_A');                                                     //  set element id
    label=$('<label class="control-label " for="blood_rwell" style="width:180px">'+labeltxt+'</label>'); //  create label for combined selects
    label.clone().appendTo($('#'+div_id));                                               //  append clone of label -
    el.clone().appendTo($('#'+div_id));                                                  //  and of select - to appropriate div
    el.find('option').remove();                                                           //  and clear select el values
    for(var val in Ndata) {$('<option />', {value: pad(val,2), text: Ndata[val]}).appendTo(el);}; // likewise create numeric select element
    el.prepend("<option value=''>--</option>");                                          //  add blank option
    el.attr('id','el_'+div_id+'_N');                                                      //  set ID
    el.clone().appendTo($('#'+div_id));                                                  //  and append clone to div
    // initialise rack well select values
    var initrackval = $("#id_"+rw_type+"_dna_sample_rack_well").val();                   //  get DB value
    $("#"+rw_type+"_rwell").attr("rackwellvalue",initrackval);                           //  and store as div attrib
    var vA=initrackval.substring(0,1);
    var vN=initrackval.substring(1);                                                     //  if value of correct format (A1-H12)
    if ((vA.match('[A-H]'))&&(vN.substring(0).match('[0-2]')&&vN.substring(1).match('[0-9]'))) {
      $("#el_"+rw_type+"_rwell_A").val(vA);                                              //   set select element values
      $("#el_"+rw_type+"_rwell_N").val(vN);
    }
    else {                                                                               //   otherwise clear values
      $("#id_"+rw_type+"_dna_sample_rack_well").val('')
      $("#"+rw_type+"_rwell").attr("rackwellvalue","")
    };
  });
  // Initialisation - set class
  $('#el_ffpe_rwell_A').addClass('ffpedna ffpednagroup');
  $('#el_ffpe_rwell_N').addClass('ffpedna ffpednagroup');
  $('#el_ff_rwell_A').addClass('ffdna ffdnagroup');
  $('#el_ff_rwell_N').addClass('ffdna ffdnagroup');
  if ($("#id_ffpe_dna_used").val()=='N') {                                               // if 'Fresh frozen' selector set to 'N'
    $('#el_ffpe_rwell_A').val('-');                                                      //   clear/disable rack well select
    $('#el_ffpe_rwell_N').val('--');
    $('#el_ffpe_rwell_A').prop("disabled", true);
    $('#el_ffpe_rwell_N').prop("disabled", true);
    }
  if ($("#id_ff_dna_used").val()=='N') {                                                 // 'FFPE' selector set to 'N'
    $('#el_ff_rwell_A').val('-');                                                        //   clear/disable rack well select
    $('#el_ff_rwell_N').val('--');
    $('#el_ff_rwell_A').prop("disabled", true);
    $('#el_ff_rwell_N').prop("disabled", true);
    }
  // update on change of rack well value
  $(".rwselect").change(function() {
    var p_el = $(this).parent().closest('div');
    p_el.removeClass('highlight');                                                       // remove highlight
    pgStatusMsg('CancelMsg');                                                            // and clear message
    p_el.attr('rackwellvalue',p_el.children('select:first-of-type').val()+ pad(p_el.children('select:nth-of-type(2)').val(),2));
  })
  // -- /rack well input: create selectors and validate ---------------------------------------------------------------

  // -- validation ----------------------------------------------------------------------------------------------------
  // uppercase (class set in layout DB table)
  $('.uppercase').css({'text-transform':'uppercase'});
  // prevent non-numeric input
  $(".numberinput").keypress(function (event) {return isNumber(event, this);});
  // tumour size
  $('#id_tumour_size').blur(function() {validate($(this),'N500')});
  // numeric µl fields
  $('.N1000').blur(function() {validate($(this),'N1000')});
  // remove any invalid input data on page load
  $('.datetimeinputsecs').each(function() {validate($(this), 'dtms', 'clear_data')});
  $('.datetimeinput').each(function() {validate($(this),'dtm', 'clear_data')});
  $('.dateinput').each(function() {validate($(this),'date', 'clear_data')});
  // set validation and type for inputs
  $('.datetimeinput').blur(function() {validate($(this),'dtm')});
  $('.dateinput').blur(function() {validate($(this),'date')});
  var el_snapstart=$("#id_ff_snap_freezing_start_dtms");
  var el_snapend=$("#id_ff_snap_freezing_end_dtms");
  el_snapstart.blur(function() {
    validate($(this), 'dtms');
    if ((!$(this).hasClass('invalid'))&&el_snapend.val()=='') {
      el_snapend.val($(this).val());
    }
  });
  el_snapend.blur(function() {
    $("#div_id_ff_snap_freezing_end_dtms").css({'border':'none'});                       // el may have border
    validate($(this), 'dtms');                                                           // from pg submit - remove
  });
  // -- /validation ---------------------------------------------------------------------------------------------------

  // -- form submit ---------------------------------------------------------------------------------------------------
  $("form").submit(function( event ) {
    $.session.set('Pgvalue', getCurrPg());                                               // store current Pg in session

    window.onbeforeunload=null;                                                          // submit - so no unload warning

    $('.rwdiv').each(function() {                                                        // validate rack well input -
      var elA=$(this).children('select:first-of-type');                                  // for each rack well div:
      var elN=$(this).children('select:nth-of-type(2)');                                 //
      if ((elA.val()==''||elN.val()=='') && (elA.val()+elN.val()!='')) {                 //  if incomplete selection
        pgStatusMsg('WARN~DNA sample rack well entry incomplete');
        $(this).addClass('highlight');                                                   //   highlight error div
        event.preventDefault();                                                          //   and prevent submit
      }
      else {                                                                             //  else
        $("#id_blood_dna_sample_rack_well").val($("#blood_rwell").attr('rackwellvalue'));//   write values to
        $("#id_ff_dna_sample_rack_well").val($("#ff_rwell").attr('rackwellvalue'));      //   DB linked els
        $("#id_ffpe_dna_sample_rack_well").val($("#ffpe_rwell").attr('rackwellvalue'));  //   for summission
      };
    });

    /*if (getdatestring(el_snapstart.val())>getdatestring(el_snapend.val())) {             // check snap freeze dates
      $("#div_id_ff_snap_freezing_end_dtms").css({'width':'160px','border':'solid 2px','border-color':'red'});
      event.preventDefault();
      pgStatusMsg('WARN~snapfreeze');
      window.onbeforeunload=function(){return warn_on_unload;};
      setTimeout(function(){el_snapend.focus();}, 1000);
    }
    else {
      el_snapend.removeClass('highlight');        NO END TIME IN V2
    }
    */
    if (getdatestring($("#id_ffpe_fixation_start_dtm").val())>getdatestring($("#id_ffpe_fixation_end_dtm").val())) {
      $("#id_ffpe_fixation_end_dtm").css({'width':'135px','border':'solid 2px','border-color':'red'});
      event.preventDefault();
      pgStatusMsg('WARN~fixationdtm');
     // window.onbeforeunload=function(){return warn_on_unload;};                      // disable for testing only
      setTimeout(function(){$("#id_ffpe_fixation_end_dtm").focus();}, 1000);
    }
    else {
      $("#id_ffpe_fixation_end_dtm").removeClass('highlight');
    }
    //alert($("#id_blood_dna_sample_rack_well").val())
    if ($("#id_blood_dna_sample_rack_well").val()=='00') {$("#id_blood_dna_sample_rack_well").val('')}
    if ($("#id_ff_dna_sample_rack_well").val()=='00') {$("#id_ff_dna_sample_rack_well").val('')}
    if ($("#id_ffpe_dna_sample_rack_well").val()=='00') {$("#id_ffpe_dna_sample_rack_well").val('')}

    //jb
    // re-enable legacy select options - otherwise they will not exist in the post data
    $("#id_ffpe_dna_extraction_method > option").each(function() {$(this).prop('disabled', false);});
    $("#id_ff_dna_extraction_method > option").each(function() {$(this).prop('disabled', false);});
    $("#id_ffpe_processing_schedule > option").each(function() {$(this).prop('disabled', false);});
    // $("# > option").each(function() {$(this).prop('disabled', false);}); // not sure what this is - removed for now JB 3 Mar
    // seems to stop lines below working ????
    $('.sample').prop('disabled', false);
    // similarly for ff/ffpe data
    $('.ff, .ffdna').prop('disabled', false);
    $('.ffpe, .ffpedna').prop('disabled', false);

  });
  // -- /form submit --------------------------------------------------------------------------------------------------

  // -- page movement control -----------------------------------------------------------------------------------------
  // wrap Pg classes for movement
  $(".Pg1").wrapAll( "<span id='pg1span'>" );
  $(".Pg2").wrapAll( "<span id='pg2span'>" );
  $(".Pg3").wrapAll( "<span id='pg3span'>" );
  $("#pg1span,#pg2span,#pg3span").css({"position":"absolute","width":"1100px","height":"600px","top":"0px"});
  $("#specform").append($("#pg1span,#pg2span,#pg3span,.PghdrC,.PghdrR"));

  // show appropriate page on doc load
  if ($.session.get('Pgvalue')=='3') {
      $("#pg1span, .Pg1").hide();
      $("#pg2span, .Pg2").hide();
      $("#pg3span, .Pg3").show();
      $("#mvR").hide();
      $("#mvL").show();
  }
  else if ($.session.get('Pgvalue')=='2') {
      $("#pg1span, .Pg1").hide();
      $("#pg3span, .Pg3").hide();
      $("#pg2span, .Pg2").show();
      $("#mvR").show();
      $("#mvL").show();
  }
  else {
      $("#pg2span, .Pg2").hide();
      $("#pg3span, .Pg3").hide();
      $("#pg1span, .Pg1").show();
      $("#mvL").hide();
      $("#mvR").show();
  }

  // left/right page move action
  $(".mv").click(function(e) {
    if (this.id=='mvL') {
      if (currPg==3) {
        $("#pg3span, .Pg3").hide('slide',{direction:'right'},mvSpeed);
        $("#pg2span, .Pg2").show('slide',{direction:'left'},mvSpeed);
        $("#mvR").show()
        newPg='2';
      }
      if (currPg==2) {
        $("#pg2span, .Pg2").hide('slide',{direction:'right'},mvSpeed);
        $("#pg1span, .Pg1").show('slide',{direction:'left'},mvSpeed);
        $("#mvL").hide()
        newPg='1';
      }
    }
    else {
      if (currPg==1) {
        $("#pg1span, .Pg1").hide('slide',{direction:'left'},mvSpeed);
        $("#pg2span, .Pg2").show('slide',{direction:'right'},mvSpeed);
        $("#mvL").show()
        newPg='2';
      }
      if (currPg==2) {
        $("#pg2span, .Pg2").hide('slide',{direction:'left'},mvSpeed);
        $("#pg3span, .Pg3").show('slide',{direction:'right'},mvSpeed);
        $("#mvR").hide()
        newPg='3';
      }
    }

    // re-hide 'measure' input if type='blocks' - will have been 'shown' on pg move
    if ($('#id_ff_sample_type').val()=='blocks') {$('#div_id_ff_sample_type_measure').hide();}
    if ($('#id_ffpe_sample_type').val()=='blocks') {$('#div_id_ffpe_sample_type_measure').hide();}
    if ($('#id_lab_sample_sent').val()=='Y') {$('#div_id_lab_sample_not_sent_reason').hide();}



    currPg=newPg;
    $.session.set('Pgvalue', currPg);

  });
  // -- /page movement control --------------------------------------------------------------------------------------------------

  //V2
  $(".unused").hide();
  $('#pgStatusMsgNode').append($('.help-block'));
  $("#id_lab_sample_not_sent_reason").css({'width':'205px'});

  // -- samples sent control ----------------------------------------------------------------------------------------------------
  if ($("#id_lab_sample_sent").val()=='N') {                                           // if 'samples sent' set to 'N'
    $('.sample').val('');                                                                 //     clear samples element data
    $('.sample').prop('disabled', true);                                                  //     and disable
    $('.samplegroup, label[for="blood_rwell"]').css({'color':'gray'});
    $('.sample_datepicker').css({'display':'none'});
    $('.rwselect').prop("disabled", true).val('-');
  }
  else{
    $("#div_id_lab_sample_not_sent_reason").hide();
  };

  $("#id_lab_sample_sent").change(function() {                                             // on cx 'Formalin fixed DNA used' value
    if ($(this).val()=='N'){                                                           //   if value = 'no'
      $('.sample').val('');                                                             //     clear  ffDNA element data
      $('.sample').prop('disabled', true);                                              //     and disable
      $('.rwselect').prop("disabled", true).val('-');
      $('.samplegroup, label[for="blood_rwell"]').css({'color':'gray'});
      $('.sample_datepicker').css({'display':'none'});
      $("#div_id_lab_sample_not_sent_reason").show();
    }
    else {                                                                               //   else
      $('.sample').prop('disabled', false);                                             //     enable ffDNA elements
      $('.rwselect').prop("disabled", false)
      $('.samplegroup').css({'color':'#000080'});
      $('.sample_datepicker').css({'display':'block'});
      $("label[for='blood_rwell']").css({'color':'#000080'});
      $("#div_id_lab_sample_not_sent_reason").hide();
      $("#id_lab_sample_not_sent_reason").val('');
    }
  });
  // -- /samples sent control ----------------------------------------------------------------------------------------------------


  // -- tumour type count and measure control V2.1--------------------------------------------------------------------------------
  setSampleTypeHeadings('ff','init')                                                     //
  setSampleTypeHeadings('ffpe','init')
  $('#id_ff_sample_type').change(function() {setSampleTypeHeadings('ff','change')})
  $('#id_ffpe_sample_type').change(function() {setSampleTypeHeadings('ffpe','change')})
  $("#id_lab_sample_sent_date").css({"width":"125px"})

  // adjust calander gif and nav bar pos for IE
  if (browser=='IE') {
    $(".ui-datepicker-trigger").css({"width":"30px","height":"27px","position":"absolute","left":"102px","top":"15px"});
    $(".ui-datepicker-trigger.ff_datepicker").css({"left":"123px","top":"15px"});
    $(".nav").css({"position":"absolute", "top":"9px","width":"500px"});
  }
  else {
    $(".ui-datepicker-trigger").css({"padding":"1px","width":"30px","height":"30px","position":"absolute","left":"105px","top":"15px"});
    $(".ui-datepicker-trigger.ff_datepicker").css({"left":"115px"});
  }
  // -- /tumour count and measure control --------------------------------------------------------------------------------------



});

// -- end document ready code

window.onbeforeunload=function(){
  $.session.set('Pgvalue', getCurrPg());
  //return warn_on_unload;  // comment out for testing only
};

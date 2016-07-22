jQuery(document).ready(function($) {
  //alert('hi')
  var thisSID=''                                                                         // current specimen ID
  var thisPID=''                                                                         // current participant ID
  var rowIndex=0                                                                         // row index used by XML buttons
  var currentXMLgenDate=''
  $.session.set('Pgvalue', '1');                                                         // reset specimen edit page number
  //-- initialize elements ------------------------------------------------------------------------------------------------------
  // set header text
  $("#GEL_header").append('Sample list');                                                // set GELCI header text
  // default buttons to disabled
  $('#rbEditSample,#rbCreateXML,#rbSendXML').prop( "disabled", true );
  // send and create XML not used currently
  $('#rbSendXML').hide();
  $('#rbCreateXML').hide();
  // add/remove classes to allow selection
  $('table tr:gt(0) td:nth-child(2)').addClass('editsample');                            // patient edit link cell
  $('.orderable.sortable.xml_status').removeClass('xml_status');
  $('.orderable.sortable.xml_sent_date').removeClass('xml_sent_date');
  // set widths
  $('#lab_sample_sent_date').css({'width':'180px'});
  $('.table1').css({'width':'1160px'});
  $('.pathology_comments').css({'width':'200px'});
  $('#rbEditSample').css({'left':'300px'});
  //$('.sample_sent_by').css({'width':'200px'}); not used
  //$('.clinical_sample_taken_dtm').css({'width':'200px'}); not used
  $('.pname').css({'width':'150px'});
  // amend table summary count title
  var res=$('.cardinality').first().text().replace('sampleviews','Samples');
  $('.cardinality').text(res);
  // set XML status text
  $('.xml_status').each(function(index, element){
    var xmlstatus=$(element).html()
    switch(xmlstatus) {
      case 'I':
        var xmltext = 'Incomplete';
        break;
      case 'R':
        var xmltext = 'Ready';
        break;
      case 'C':
        var xmltext = 'Created';
        break;
      case 'S':
        var xmltext = 'Sent';
        break;
    }
    $(element).html(xmltext)
  });
  // sendXML button init
  //$('.xml_status').each(function(index, element){if ($(element).html()=='Ready') {$('#rbCreateXML').prop( "disabled", false );}});

  //-- /initialize elements ------------------------------------------------------------------------------------------------------

  //-- add specimen select link column -------------------------------------------------------------------------------------------
  $('table').find('tr').each(function(){
      $(this).find('td').eq(9).after('<td class="rbcell"></td>');                        //   add select cell after Nth col
   });
   
  $('table').find('tr').each(function(){ $(this).find('th').eq(-1).after('<th>Select</th>'); });   //   and header
      
  //$('.xml_sent_date').next().addClass('rbcell');                                       //   add class to select cells :not needed see 2 lines up
       
  $('.rbcell').each(function(index, element){                                            //   for each select cell -
    var SID2=$(element).siblings('.clinical_sample_id').html()                           //     get the current SID, PID and
    var PID2=$(element).siblings('.pid_fk').html()                                       //     XML status
    var XMLstatus=$(element).siblings('.xml_status').html()                              //     and add a radio button to the select cell
    $(element).append('<input type="radio" id=' + SID2 + ' pid= ' + PID2 + ' XMLstatus = ' + XMLstatus + ' class="rbutton">')
  });
  //-- /add specimen select link column -------------------------------------------------------------------------------------------

  // specimen select click function
  $('.rbutton').click(function() {
                   
    thisSID=$(this).attr('id');                                                          //  get current SID
    thisPID=$(this).attr('pid');
    //alert('click SID:'+thisSID+'  PID:'+thisPID)
    currentXMLgenDate=$(this).parent().prev().prev()                                     // get XMLgendate element
                                                                                         // note: this doesn't work ??? currentXMLgenDate=$(this).parent().closest('td').find('.xml_generated_date')
    var thisXMLstatus=$(this).attr('XMLstatus');                                         // get current XMLstatus
  
    $('.rbutton:not(#'+thisSID+')').attr('checked', false);                              // uncheck all other RBs
    //alert('thisXMLstatus:'+thisXMLstatus)

    switch(thisXMLstatus) {                                                              // enable/disable buttons as per XML status
    case 'I':
    case 'Incomplete':
      $('#rbEditSample').prop( "disabled", false );
      //$('#rbCreateXML).prop( "disabled", true );
      break;
    case 'R':
    case 'Ready':
      $('#rbEditSample, #rbCreateXML').prop( "disabled", false );
      //$('#rbSendXML').prop( "disabled", true );
      break;
    case 'C':
    case 'Complete':
      $('#rbEditSample, #rbCreateXML').prop( "disabled", false );
      break;
    case 'S':
    case 'Sent':
      //$('#rbSendXML').prop( "disabled", false );
      $('#rbEditSample, #rbCreateXML').prop( "disabled", true );
      break;      
    }

    //$('#rbCreateXML, #rbSendXML').prop( "disabled", true );  // XML DISABLED TEMPORARILY - REMOVE THIS LINE LATER .... JB 16/12/15
    $('#rbCreateXML').hide()
  });

  // 'Edit Sample' button click function
  $('#rbEditSample').click(function() {
  	//window.location.href='/specimen/add/None/'+thisSID+'/' ;
  	window.location.href='/specimen/add/'+thisPID+'/'+thisSID+'/' ;
  })


/*
  // 'Create XML' button click function
  $('#rbCreateXML').click(function() {
    var SIDlist=[]
    $('.xml_status').each(function(index, element){                                      // create list of 'ready' SIDs
      var xmlstatus=$(element).html()
      if (xmlstatus=='Ready') {
        item=$(element).prevAll('td.clinical_sample_id').html()
        SIDlist.push(item)
      }
    })
    var URL='/xmlgenerate/'
    var string=JSON.stringify(SIDlist)
    $.ajax({                                                                             // call XML generate function
      type: "GET",
      url: URL,
      cache: false,
      async: false,
      dataType: "json",
      traditional: true,
      data: {'sidlist': string}
    })                                                                                   // which will update XML status ..
    window.location.href='/specimen/list/';                                              // .. so reload page
  })
*/


})
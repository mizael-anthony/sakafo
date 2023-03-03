var idModalEntity = "#modal-entity";
var idTableEntity = "#entity-table";
var idTableHS = "#hs-table";
									  
var idTableRecap = "#recap-table";
var idTableRecapDir = "#dir-recap-table";
var idTableContent = "#content-table";
var idTableauBord = "#tableau-bord";
var idPanelView = "#pannel-view";
var idMessage = "#messages";

var clCreateEntity = ".js-create-entity";
var clUpdateEntity = ".js-update-entity";
var clDeleteEntity = ".js-delete-entity";
var clUploadEntity = ".js-upload-entity";
var clValidateEntity = ".js-validate-entity";

var clCreateFormEntity= ".js-entity-create-form";
var clUpdateFormEntity= ".js-entity-update-form";
var clDeleteFormEntity= ".js-entity-delete-form";
var clValidateFormEntity= ".js-entity-validate-form";

/*------ performLoading ------*/
function performLoading (btn, idModal) { 
  
  var successLoadForm = function(data){
    $(idModal + " .modal-content").html(data.html_form).promise().done(function() {
      console.log("successLoadForm");
      Helpers.ShowModalEntity();
    });
  };

  $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    success: successLoadForm
  });
}

/* Functions */
  var loadForm = function () {
    var btn = $(this);
    Helpers.Loading(btn, idModalEntity);
  };
  
  var saveForm = function () {
    var form = $(this);
    console.log(form);
    var dataToSend = form.serialize();
    console.log(dataToSend);
    var successSaveForm = function(data){
      if (data.form_is_valid) {
        if (typeof data.html_message != 'undefined') {
          $(idMessage).html(data.html_message);
        }
        else {
          if (typeof data.url_redirect != 'undefined') {
            // Recharger la page entière
            location.href = data.url_redirect;
          } else {
            // Recharger le contenu de la table
            $(idTableEntity + " tbody").html(data.html_content_list);
            $("#paginator_id").html(data.html_content_paginator);
          }
        }

        //Fermer le pop-up principal
        Helpers.HideModalEntity();
      }
      else {
        Helpers.ShowError(data);             
      }
    };

    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',      
      success: successSaveForm
    });
    return false;
  };

//méthode permettant de detecter l'action en cours : Create, update, validate, delete ...
function get_action(url){
  if (url.indexOf("create") !=-1) {
    return "create"
  }
  if (url.indexOf("update") !=-1) {
    return "update"
  }
  if (url.indexOf("delete") !=-1) {
    return "delete"
  } 
  if (url.indexOf("validate") !=-1) {
    return "validate"
  }  
}
/* Binding */

// Create entity
$(clCreateEntity).click(loadForm); /* Creation d'un objet hors table*/
$(idModalEntity).on("submit", clCreateFormEntity, saveForm);

// Update entity
$(clUpdateEntity).on("click", loadForm); /* Ajouté le 2018-09-24 pour la Gestion des Notifications */
$(idTableEntity).on("click", clUpdateEntity, loadForm);
$(idModalEntity).on("submit", clUpdateFormEntity, saveForm);

// Delete entity
$(idTableEntity).on("click", clDeleteEntity, loadForm);
$(idModalEntity).on("submit", clDeleteFormEntity, saveForm);

// Validate entity
$(idTableEntity).on("click", clValidateEntity, loadForm);

// Upload entity
$(clUploadEntity).on("click", loadForm); /*Ajoute le 2018-11-26 pour UPLOAD HORS TABLE*/
$(idTableEntity).on("click", clUploadEntity, loadForm);

var Helpers = {
  Loading: performLoading,
  MsgBoxOnYesClickedJs: function(){},
  MsgBoxOnNoClickedJs: function(){
    $("#modal-entity").css("opacity","1");
    return false;},
  ShowMessageAlert: function (message, onYesFunction) {
      if (onYesFunction != null) {
        Helpers.MsgBoxOnYesClickedJs = onYesFunction;
      }
      
      $("#avertissement-message").html(message).promise().done(function() {
        $("#modal-avertissement").modal("show").draggable({ handle: ".modal-header" }); //Popup Movable
      });
  },
  ShowModalEntity: function(){
     $(idModalEntity).css("opacity","1");
    return $(idModalEntity).modal("show").draggable({ handle: ".modal-header" }); //Popup Movable
  },
  HideModalEntity: function(){
    return $(idModalEntity).modal("hide");
  },
  OkErrorOnClickedJs: function(){
    $("#modal-entity").css("opacity","1");
    return $("#modal-erreur").modal("hide");
  },
  ShowError: function (data) {    
       $("#erreur-message").html(data.html_form).promise().done(function() {
          $("#modal-entity").css("opacity","0.75");
          $("#modal-erreur").modal("show").draggable({ handle: ".modal-header" }); //Popup Movable
       });
  },
  ShowErrorSpecific: function (data) {    
       $("#erreur-message").html(data.message).promise().done(function() {
          $("#modal-entity").css("opacity","0.75");
          $("#modal-erreur").modal("show").draggable({ handle: ".modal-header" }); //Popup Movable
       });
  },
  ShowErrorJQuery: function (message) {
    $.confirm({
      title: 'ERP - Erreur rencontrée',
      content: message,
      type: 'red',
      typeAnimated: true,
      draggable: true,
      buttons: {
        close: function () {
        }
      }
    });
  },  
  ShowModalNotification: function (data) {   
    $("#notification-message").html(data.html_form).promise().done(function() {
      $("#modal-entity").css("opacity","0.75");
      $("#modal-notification").modal("show").draggable({ handle: ".modal-header" }); //Popup Movable
    });
  },
  ExportTitle: function(){
    //Gestion titre export
    var defaultTitle = 'GCTO';
    var pageTitle = $(".card-title").text();
    if(pageTitle != "")
    {
      defaultTitle = pageTitle;
    }
    return defaultTitle;
  },

  BuildDropdown: function(result, dropdown, emptyMessage, selected_id, text_field, text_field_other='')
  {
      //Methode helpers pour remplir le dropdown
      // Vider le dropdown
      dropdown.html('');

      // Initialiser le dropdown
      dropdown.append('<option value="">' + emptyMessage + '</option>');

      // Test si le résulat n'est pas null
      if(result != '')
      {           

          // Parcourir le résultat et remplir le dropdown
          $.each(result, function(k, v) {
              lib2 = '';
              if (text_field_other!='') {
                lib2 = ' - ' + v[text_field_other];
              }
              if (selected_id != "None" && selected_id >=0 &&  selected_id == v.id) {
                  //Metre le selected value
                  dropdown.append('<option value="' + v.id + '" selected>' + v[text_field] + lib2 + '</option>');
              } else {
                  dropdown.append('<option value="' + v.id + '">' + v[text_field] + lib2 + '</option>');
              }
          });
      }
  },

//---------------------------------------------
//----------------- DATE PICKER ---------------
//---------------------------------------------
  /**
  Datetime picker Jquery
  selected_id : champs date
  init_date: la date par défaut si indiquée
  */
  DatePicker: function(selected_id, init_date=null)
  {
    if (init_date) { init_date = init_date }

    $( "#"+selected_id ).datepicker({
      firstDay: 1, // Start with Monday
      todayHighlight: true,
      format: 'dd/mm/yyyy',
    })
  },

  isValidDate: function(s) {
    var bits = s.split('/');
    var d = new Date(bits[2] + '/' + bits[1] + '/' + bits[0]);
    return !!(d && (d.getMonth() + 1) == bits[1] && d.getDate() == Number(bits[0]));
  },

  /*DATE DU JOUR en FR*/
  GetDateTodayFr: function () {
    var d = new Date();
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (day < 10) {
        day = "0" + day;
    }
    if (month < 10) {
        month = "0" + month;
    }
    var date = day + "/" + month + "/" + year;

    return date;
  },

  /*DATE NOUVEL AN de l'année en cours en FR*/
  GetNewYearToDateFr: function () {
    var d = new Date();
    var year = d.getFullYear();
    
    return "01/01/" + year;
  },

  /*ANNE en cours*/
  GetCurrentYear: function () {
    var d = new Date();
    return d.getFullYear();
  },

  /*DATE du 1er mois en cours en FR*/
  GetFirstCurrentMonthToDateFr: function () {
    var d = new Date();
    var month = d.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    var year = d.getFullYear();
    
    return "01/" + month + "/" + year;
  },

  //---------------------------------------------
  //----------------- TIME PICKER ---------------
  //---------------------------------------------
  /**
  Time picker Jquery
  selected_id : champs date
  minTime : temps minimum -> '05:00:00'
  maxHour: heure maximum -> vers 16 h
  StartH: heure début -> 12 h
  StartM: minute début -> 30 mn
  interval_minute: intervalle en minute -> tous les 5mn
  */
  TimePicker: function(selected_id, minTime, maxHour, StartH, StartM, interval_minute)
  {
    //Définir spécifiquement le time picker AM
    $( "#"+selected_id ).timepicker({ 
      timeFormat: 'HH:mm',
      minTime: minTime,
      maxHour: maxHour,
      startTime: new Date(0,0,0,StartH,StartM,0),
      disableFocus: true,
      template: 'dropdown',
      interval: interval_minute,
      zindex: 9999999, //Affichage sur modal !! IMPORTANT !!
    })
  },

  //---------------------------------------------
  //----------------- DATA TABLE ----------------
  //---------------------------------------------
  LoadDataTable: function()
  {
    var thArray = [];
    $('#entity-table thead th').each( function () {
      var title = $(this).text();
      if (title != '') // Ne pas afficher l'input les IDs cachés
        $(this).html( title + '<br><input type="text" class="search-input" placeholder="Chercher ..." title="Par ' + title + '" />' );
    } );
    
    // Très IMORTANT pour la pagination
    $.fn.dataTable.ext.classes.sPageButton = 'button button-primary';

    var table = $(idTableContent).DataTable({
      language: {
        "info": "_TOTAL_ / _MAX_ élément(s) affiché(s)&nbsp;&nbsp;",
        "infoEmpty": "Aucun élément à afficher",
        "search": "Recherche",
        "infoFiltered": "",
        "emptyTable": "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrement&nbsp;&nbsp;</span>",
        "loadingRecords":   "En chargement...",
        "processing":       "En traitement...",
        "zeroRecords":      "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrements correspondants trouvés&nbsp;&nbsp;</span>",
        "paginate": {
          "previous": '<i class="fa fa-chevron-left"></i>',
          "next": '<i class="fa fa-chevron-right"></i>',
        }
      },

      paging :true,
      lengthChange: false,
      bFilter : true,
      ordering : true,
      info: true,
      targets: 0,
      responsive: false,
      pageLength: 27,
      
      //dom: 'lrtip',
      dom: 'Bfrtip',
      buttons: [
        // { "extend": 'excel', "text":'',"className": 'fa fa-file-excel-o texte-vert' },
        // { "extend": 'pdf', "text":'',"className": 'fa fa-file-pdf-o texte-rouge' },
        // { "extend": 'print', "text":'imprimer',"className": 'btn btn-default btn-xs' },
      ],
      //searching: false,

      // Formatter l'affichage des column view
      // responsive: {
      //   details: {
      //       renderer: function ( api, rowIdx, columns ) {
      //           var data = $.map( columns, function ( col, i ) {
      //               let title = col.title.split('<br>')[0]; // Ne pas afficher les recherche en mode expand
      //               return col.hidden ? title + ': ' + col.data + '<hr width="25%" align=left>' : '';
      //           } ).join('');
      //           return data ? data : false;
      //       }
      //   }
      // }
    });
    
    var table = $(idTableHS).DataTable({
      language: {
        "info": "_TOTAL_ / _MAX_ élément(s) affiché(s)&nbsp;&nbsp;",
        "infoEmpty": "Aucun élément à afficher",
        "search": "Recherche",
        "infoFiltered": "",
        "emptyTable": "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrement&nbsp;&nbsp;</span>",
        "loadingRecords":   "En chargement...",
        "processing":       "En traitement...",
        "zeroRecords":      "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrements correspondants trouvés&nbsp;&nbsp;</span>",
        "paginate": {
          "previous": '<i class="fa fa-chevron-left"></i>',
          "next": '<i class="fa fa-chevron-right"></i>',
        }
      },

      paging :true,
      lengthChange: false,
      bFilter : true,
      ordering : true,
      info: true,
      targets: 0,
      responsive: false,
      pageLength: 15,
      
      //dom: 'lrtip',
      dom: 'Bfrtip',
      buttons: [
        { "extend": 'excel', "text":'',"className": 'fa fa-file-excel-o texte-vert',
          exportOptions: {
            columns: ':visible',
            format: {
                body: function(data, row, column, node) {
                    data = $('<p>' + data + '</p>').text();
                    return $.isNumeric(data.replace(',', '.')) ? data.replace(',', '.') : data;
                }
            }
        }
        },
        { "extend": 'pdf', "text":'',"className": 'fa fa-file-pdf-o texte-rouge' },
        // { "extend": 'print', "text":'imprimer',"className": 'btn btn-default btn-xs' },
      ],
      //searching: false,

      // Formatter l'affichage des column view
      // responsive: {
      //   details: {
      //       renderer: function ( api, rowIdx, columns ) {
      //           var data = $.map( columns, function ( col, i ) {
      //               let title = col.title.split('<br>')[0]; // Ne pas afficher les recherche en mode expand
      //               return col.hidden ? title + ': ' + col.data + '<hr width="25%" align=left>' : '';
      //           } ).join('');
      //           return data ? data : false;
      //       }
      //   }
      // }
    });
    
    var table = $(idTableRecap).DataTable({
      language: {
        "info": "_TOTAL_ / _MAX_ élément(s) affiché(s)&nbsp;&nbsp;",
        "infoEmpty": "Aucun élément à afficher",
        "search": "Recherche",
        "infoFiltered": "",
        "emptyTable": "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrement&nbsp;&nbsp;</span>",
        "loadingRecords":   "En chargement...",
        "processing":       "En traitement...",
        "zeroRecords":      "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrements correspondants trouvés&nbsp;&nbsp;</span>",
        "paginate": {
          "previous": '<i class="fa fa-chevron-left"></i>',
          "next": '<i class="fa fa-chevron-right"></i>',
        }
      },

      paging :false,
      lengthChange: false,
      bFilter : true,
      ordering : true,
      info: true,
      targets: 0,
      responsive: false,
      pageLength: 8,
      "scrollX": true,
      "scrollY": 350,
      "scroller": true,
      //dom: 'lrtip',
      dom: 'Bfrtip',
      buttons: [
        { "extend": 'excel', "text":'',"className": 'fa fa-file-excel-o texte-vert' },
        // { "extend": 'pdfHtml5', "orientation":'landscape',"pageSize":'A1', "text":'',"className": 'fa fa-file-pdf-o texte-rouge' },
        // { "extend": 'print', "text":'imprimer',"className": 'btn btn-default btn-xs' },
      ],
      searching: true,
    });
    
    var table = $(idTableRecapDir).DataTable({
      language: {
        "info": "_TOTAL_ / _MAX_ élément(s) affiché(s)&nbsp;&nbsp;",
        "infoEmpty": "Aucun élément à afficher",
        "search": "Recherche",
        "infoFiltered": "",
        "emptyTable": "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrement&nbsp;&nbsp;</span>",
        "loadingRecords":   "En chargement...",
        "processing":       "En traitement...",
        "zeroRecords":      "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrements correspondants trouvés&nbsp;&nbsp;</span>",
        "paginate": {
          "previous": '<i class="fa fa-chevron-left"></i>',
          "next": '<i class="fa fa-chevron-right"></i>',
        }
      },

      paging :false,
      lengthChange: false,
      bFilter : true,
      ordering : true,
      info: true,
      targets: 0,
      responsive: false,
      pageLength: 8,
      "scrollX": true,
      "scrollY": 350,
      "scroller": true,
      //dom: 'lrtip',
      dom: 'Bfrtip',
      buttons: [
        { "extend": 'excel', "text":'',"className": 'fa fa-file-excel-o texte-vert' },
        { "extend": 'pdfHtml5', "orientation":'landscape',"pageSize":'A1', "text":'',"className": 'fa fa-file-pdf-o texte-rouge' },
        // { "extend": 'print', "text":'imprimer',"className": 'btn btn-default btn-xs' },
      ],
      searching: true,
    });

    var table = $(idTableEntity).DataTable({
      language: {
        "info": "_TOTAL_ / _MAX_ élément(s) affiché(s)&nbsp;&nbsp;",
        "infoEmpty": "Aucun élément à afficher",
        "search": "Recherche",
        "infoFiltered": "",
        "emptyTable": "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrement&nbsp;&nbsp;</span>",
        "loadingRecords":   "En chargement...",
        "processing":       "En traitement...",
        "zeroRecords":      "<span class='bg-warning'>&nbsp;&nbsp;Aucun enregistrements correspondants trouvés&nbsp;&nbsp;</span>",
        "paginate": {
          "previous": '<i class="fa fa-chevron-left"></i>',
          "next": '<i class="fa fa-chevron-right"></i>',
        }
      },
      // initComplete: function () {
      //     this.api().columns() function () {
      //         var column = this;
      //         var select = $('<select><option value=""></option></select>')
      //             .appendTo( $(column.header()).empty() )
      //             .on( 'change', function () {
      //                 var val = $.fn.dataTable.util.escapeRegex(
      //                     $(this).val()
      //                 );

      //                 column
      //                     .search( val ? '^'+val+'$' : '', true, false )
      //                     .draw();
      //             } );

      //         column.data().unique().sort().each( function ( d, j ) {
      //             select.append( '<option value="'+d+'">'+d+'</option>' )
      //         } );
      //     } );
      // },

      paging :true,
      lengthChange: false,
      bFilter : true,
      ordering : true,
      info: true,
      targets: 0,
      responsive: true,
      pageLength: 12,
      
      //dom: 'lrtip',
      dom: 'Bfrtip',
      buttons: [
        // { "extend": 'excel', "text":'',"className": 'fa fa-file-excel-o texte-vert',
        //     exportOptions: {
        //       columns: ':visible',
        //       format: {
        //           body: function(data, row, column, node) {
        //               data = $('<p>' + data + '</p>').text();
        //               return $.isNumeric(data.replace(',', '.')) ? data.replace(',', '.') : data;
        //           }
        //       }
        //   }
        // },
        // { "extend": 'pdf', "text":'',"className": 'fa fa-file-pdf-o texte-rouge' },
        // { "extend": 'print', "text":'imprimer',"className": 'btn btn-default btn-xs' },
      ],
      //searching: false,

      // Formatter l'affichage des column view
      responsive: {
        details: {
            renderer: function ( api, rowIdx, columns ) {
                var data = $.map( columns, function ( col, i ) {
                    let title = col.title.split('<br>')[0]; // Ne pas afficher les recherche en mode expand
                    return col.hidden ? title + ': ' + col.data + '<hr width="25%" align=left>' : '';
                } ).join('');
                return data ? data : false;
            }
        }
      }
    });
    

    // Apply the search
    table.columns().every(function () {
      var that = this;
      $('input', this.header()).on('keyup change', function () {
        if (that.search() !== this.value) {
          that.search(this.value).draw();
        }
      });
      $('input', this.header()).on('click', function () {
        return false;
      });
    });
    
    new $.fn.dataTable.FixedHeader( table );
    
  },

  LoadDataTableauBord: function()
  {
    var table = $(idTableauBord).DataTable({
      order: [],
      columnDefs: [ { orderable: false, targets: [0] } ],

      paging :false,
      bFilter : false,
      ordering : false,
      searching : false,
      info: false,
      responsive: true,
      
      dom : 'l<"#action_add_element">frtip',
    });
  },

  LoadPanelView: function()
  {
    var table = $(idPanelView).DataTable({
      order: [],
      columnDefs: [ { orderable: false, targets: [0] } ],

      paging :false,
      bFilter : false,
      ordering : false,
      searching : false,
      info: false,
      responsive: true,
      
      dom : 'l<"#action_add_element">frtip',
    });
  },

}

$(document).ready(function(){
  
  
  //Tabeau de bord  
  Helpers.LoadDataTableauBord();

  //Table List standard
  Helpers.LoadDataTable();
  
  
  //Table pour Panel View
  Helpers.LoadPanelView();
});

//---------------------------------------------
//-------------- FORMATAGE DES CHAMPS  --------
//---------------------------------------------

//Mettre un champs input text en majiscule
function To_Majiscule(id_input) {
  var someInput = document.querySelector(id_input);
  someInput.addEventListener('input', function () {
    someInput.value = someInput.value.toUpperCase();
  });
}

//---------------------------------------------
//------ LISTE: RECHERCHE MUTI-CRITERES -------
//---------------------------------------------
$(document).ready(function(){
    $('#btn_search').keypress(function(e){
      if(e.keyCode==13)
        $('#btn_search').click();
    });
});

//---------------------------------------------
//----------------- UPLOAD FILE ---------------
//---------------------------------------------
function getFileUploadName(elt, select) {
  var fn = $(elt).val();
  var filename = fn.match(/[^\\/]*$/)[0]; // remove C:\fakename
  
  $('#'+select).html("<b>"+filename+"</b>");
}

//---------------------------------------------
//------ MESSAGE VALIDATION ANYWHERE --------
//---------------------------------------------
function _ValidateAnywhere(pk, url, message)
{
  $("#modal-entity").css("opacity","0.75");
  var onYesClicked = function(){
    $("#modal-entity").css("opacity","1");
    $.ajax({
      url : url,
      type : "POST",
      data : {
        "id" : pk,
      },
      dataType : "json",
      success : function(data){
        if (data.error) {
           Helpers.ShowErrorSpecific(data);
        } else {
          //fermer le pop-up principal
          Helpers.HideModalEntity();
        
          //Ouvrir la liste (avec paginator)
          location.href = data.url_redirect;
        }
      }
    });
      
    return true;
  }
  Helpers.ShowMessageAlert(message, onYesClicked);
}
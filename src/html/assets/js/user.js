var formApp = {};

function createRole(){
  if(!$('#name').val()){
    showMSG('Please enter role', 'warning');
    return;
  }
  
  postRequest('saveRoleForm', '/Role', 'createRoleCallBack');
};

function createRoleCallBack(r, fid){
  if(r.status !='SUCCESS'){return}
  
  $('#table_body').prepend('<tr><td>'+r.data.name+'</td><td>'+r.data.description+'</td></tr>')
};

var formApp = {};

formApp.showCreateFormGroupPop = function() {
  $('#create_form_group')[0].reset();
  $('#form_group_popup').modal('show');
};

formApp.createFormGroup = function() {
  var g = $('#new_form_group').val();
  if (g == '') {
    toastr.error('Fill Name');
    return;
  }

  createPostRequest('create_form_group', '/FormGroupCreate',
      'formApp.createFormGroupCallBack');

};

formApp.createFormGroupCallBack = function(response, formId) {
  var responseData = $.parseJSON(response.message);
  $('#form_group').append(
      '<option value="' + responseData.key + '">' + responseData.name
          + '</option>');
  $('#form_group_popup').modal('hide');
};

formApp.addNewFeild = function() {
  $('#form_feild_container').append($('#form_feild_dom').html());
};

formApp.removeFeild = function(elm) {
  elm.parentNode.parentNode.remove();
};

formApp.feildTypeOnChange = function(elem) {
  if (elem.value == 'number') {
    $(elem.parentNode.parentNode.parentNode).find(
        '.number-validation, .default-validation').show();
    $(elem.parentNode.parentNode.parentNode).find(
        '.phone-validation, .option-validation, .subform-validation').hide();
  } else if (elem.value == 'phone') {
    $(elem.parentNode.parentNode.parentNode).find('.phone-validation').show();
    $(elem.parentNode.parentNode.parentNode)
        .find(
            '.number-validation, .option-validation, .default-validation, .subform-validation')
        .hide();
  } else if (elem.value == 'multichoice' || elem.value == 'radio'
      || elem.value == 'dropdown' || elem.value == 'filtereddropdown') {
    $(elem.parentNode.parentNode.parentNode).find('.option-validation').show();
    $(elem.parentNode.parentNode.parentNode)
        .find(
            '.number-validation, .phone-validation, .default-validation, .subform-validation')
        .hide();
  } else if (elem.value == 'subform') {
    $(elem.parentNode.parentNode.parentNode).find('.subform-validation').show();
    $(elem.parentNode.parentNode.parentNode)
        .find(
            '.number-validation ,.phone-validation, .option-validation, .default-validation')
        .hide();
  } else {
    $(elem.parentNode.parentNode.parentNode)
        .find(
            '.number-validation ,.phone-validation, .option-validation, .default-validation, .subform-validation')
        .hide();
  }

};

formApp.addMoreOption = function(elem) {
  optionHtml = [ '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 padding-lr-0  pd-top-7x"><label class="col-lg-3 col-md-3 col-sm-3 col-xs-12">Option</label><div class="col-lg-8 col-md-8 col-sm-8 col-xs-12">' ];
  optionHtml
      .push('<input type="text" name="option" class="form-control" placeholder="Option" value=""></div>');
  optionHtml
      .push('<div class="col-lg-1 col-md-1 col-sm-1 col-xs-12"> <button class="pull-rigth" onclick="formApp.removeMoreOption(this)" type="button"><i class="fa fa-trash-o fa-2x" ></i></button></div></div>');
  $(optionHtml.join('')).insertBefore(elem);
};

formApp.removeMoreOption = function(btn) {
  btn.parentNode.parentNode.remove();
};

formApp.getAllField = function() {
  var fieldDataArray = [];
  $('#form_feild_container').children('.well').each(function() {
    data = $(this).serializeArray();
    fieldDataArray.push(data);
  });

  console.log(fieldDataArray);
  return fieldDataArray;
};

function sectionSubProcess(item) {
  var sectionFields = [];
  $(item).find('.well').each(function() {
    data = $(this).serializeArray();
    sectionFields.push(data);
  });
  return sectionFields;
}

formApp.getAllSection = function() {
  var fieldDataArray = [];
  $('#form_feild_container').children('.section-form').each(function() {
    section = $(this).serializeArray();
    var sectionFields = sectionSubProcess(this.lastElementChild);
     
    fieldDataArray.push({'setcion':section[0], 'sectionFields': sectionFields});
  });

  console.log(fieldDataArray);
  return fieldDataArray;
};

formApp.saveUpdateForm = function() {
  if ($('#form_title').val() == '') {
    toastr.error('Form title missing');
    return;
  }
  if ($('#form_description').val() == '') {
    toastr.error('Form description missing');
    return;
  }

  formData = $('#create_update_form').serializeArray();
  var slider = $('#form_slider').val();
  if(slider == 'OFF'){
    formFieldArr = formApp.getAllField()
  } else{
    formFieldArr = formApp.getAllSection()
  }
  formData.push({
    name : 'formField',
    value : JSON.stringify(formFieldArr)
  });
  callBack = 'formApp.updateFormCallBack';
  if ($('#form_key').val() == '') {
    callBack = 'formApp.saveFormCallBack';
  }
  customDataPostRequest('/FormCreateUpdate', formData, callBack);
};

formApp.saveFormCallBack = function(response, formId) {
  var responseData = $.parseJSON(response.message);
  var table = $('#form_list_table').DataTable();
  var newRow = {
    "DT_RowId" : responseData.key,
    "title" : responseData.title,
    "description" : responseData.description,
    "form_froup_name" : responseData.form_froup_name,
    "form_froup" : responseData.form_froup,
    "layout" : responseData.layout,
    "formtype" : responseData.formtype
  }
  var rowNode = table.row.add(newRow);
  rowNode.draw().node();
  formApp.backFormRecord();
};

formApp.updateFormCallBack = function(response, formId) {
  var responseData = $.parseJSON(response.message);
  var table = $('#form_list_table').DataTable();
  var newRow = {
    "DT_RowId" : responseData.key,
    "title" : responseData.title,
    "description" : responseData.description,
    "form_froup_name" : responseData.form_froup_name,
    "form_froup" : responseData.form_froup,
    "layout" : responseData.layout,
  }
  table.row('#' + responseData.key).data(newRow).draw();
  formApp.backFormRecord();
};

formApp.backFormRecord = function() {
  $('#create_update_form')[0].reset();
  $('#form_key').val('');
  $('#create_update_form_dom, #module_entity_back_dom_link_btn').hide();
  $('#form_records_dom, #module_entity_create_dom_link_btn').show();
};

formApp.createFormRecord = function() {
  $('#create_update_form')[0].reset();
  $('#form_key').val('');
  $('#form_feild_container').html('');
  $('#create_update_form_dom, #module_entity_back_dom_link_btn, .new-field-btn').show();
  $('#form_records_dom, #module_entity_create_dom_link_btn, .new-section-btn').hide();
};

formApp.editSekectedFormDataRow = function(dataTableRow) {
  var rowData = dataTableRow.data();
  $('#create_update_form')[0].reset();
  $('#create_update_form_dom, #module_entity_back_dom_link_btn').show();
  $('#form_records_dom, #module_entity_create_dom_link_btn').hide();
  $('#form_key').val(rowData.DT_RowId);
  $('#form_title').val(rowData.title);
  $('#form_description').val(rowData.description);
  $('#form_group').val(rowData.form_froup).attr('selected', 'selected');
  $('#form_layout').val(rowData.layout).attr('selected', 'selected');
  $('#form_category').val(rowData.formtype).attr('selected', 'selected');
  $('#form_feild_container')
      .html(
          '<div style="text-align:center"><p>Please wait form fields are loading...</p><i class="fa fa-spinner fa-spin fa-fw fa-3x"></i></div>');
  createGetRequest('', '/FormGetFieldXML?key=' + rowData.DT_RowId,
      'formApp.getFormXmlCallBack');
};

formApp.getFormXmlCallBack = function(response, fId) {
  $('#form_slider').val(response.form_slider).attr('selected', 'selected');
  if(response.form_slider=='OFF') {
    $('.new-field-btn').show();
    $('.new-section-btn').hide();
  } else {
    $('.new-section-btn').show();
    $('.new-field-btn').hide();
  }
  $('#form_feild_container').html(response.message);
  
};

formApp.addNewSection = function() {
  $('#form_feild_container').append($('#form_section_dom').html());
};

formApp.sectionTypeOnChange = function(elem) {
  if (elem.value == 'switch') {
    $(elem.parentNode.parentNode.parentNode).find('.switch-validation').show();
    $(elem.parentNode.parentNode.parentNode).find('.option-validation').hide();
  } else {

    $(elem.parentNode.parentNode.parentNode).find('.switch-validation').hide();
    $(elem.parentNode.parentNode.parentNode).find('.option-validation').show();
  }

};

formApp.addSectionField = function(elem) {
  $($('#form_feild_dom').html()).insertBefore(elem);  
};

formApp.clearFormSectionFieldData = function(elem) {
  $('#form_feild_container').html('');
  
  if(elem.value=='OFF') {
    $('.new-field-btn').show();
    $('.new-section-btn').hide();
  } else {
    $('.new-section-btn').show();
    $('.new-field-btn').hide();
  }
  
};



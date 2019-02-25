"use strict";
function formToJSON( formData ) {
  var object = {};
  formData.forEach(function(value, key, element){

    object[key] = value;
  });
  var json_obj = JSON.stringify(object);

  return object;
};
// Loading
//----------------------------------------------
function remove_loading($form, options)
{
  $form.find('[type=submit]').removeClass('error success');
  $form.find('.login-form-main-message').removeClass('show error success').html('');
};

function form_loading($form, options)
{
  $form.find('[type=submit]').addClass('clicked').html(options['btn-loading']);
};

function form_success($form, options)
{
  location.reload();
  $form.find('[type=submit]').addClass('success').html(options['btn-success']);
  $form.find('.login-form-main-message').addClass('show success').html(options['msg-success']);
};

function form_failed($form, options)
{
  $form.find('[type=submit]').addClass('error').html(options['btn-error']);
  $form.find('.login-form-main-message').addClass('show error').html(options['msg-error']);
};

// Dummy Submit Form (Remove this)
//----------------------------------------------
// This is just a dummy form submission. You should use your AJAX function or remove this function if you are not using AJAX.
function submit_form($form, dest_url, formData, options)
{
  if($form.valid())
  {
    form_loading($form, options);

    //var json_obj = formToJSON( formData );
    //console.log(json_obj);
    //formData.append('form_json', json_obj);
    $.ajax({
      method: "POST",
      url: dest_url,
      data: formData,
      processData: false,
      contentType: false,
      cache: false,
      success: form_success( $form, options)//,
    });

    setTimeout(function() {
      form_success($form, options);
    }, 2000);
  }
};

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


var Formy = function(form) {
  this.submitting = false;
  this.posted = false;
  this.form = form;
  this.error = false;

  this.submitForm = function() {
    var Formy = this;

    // deterimine if form is already submitted;
    if(Formy.submitting) return;
    Formy.form.find(':input[type=submit]').prop('disabled', true);
    Formy.submitting = true;
    $('.loading').show();
    $('.checkmark').hide();

    //construct the basic payload for postem.
    let payload = {
      data: Formy.getFormElements(),
      query: Formy.getQueryParams()
    }

    var endpoint = Formy.form.attr('action');
    Formy.postem(endpoint, payload)
    .then(function(result){
      Formy.posted = true;
      Formy.submitting = false;
      $(".loading").hide();
      $(".checkmark").show();
      Formy.form.find(':input[type=submit]').prop('disabled', false);
      console.log(result);
    })

  },//submit form

  //parse the incoming query string to a js object
  this.getQueryParams = function(){
  if(document.location.search){
    return (document.location.search)
    .replace(/(^\?)/,'')
    .split("&")
    .map(function(n){return n = n.split("="),this[n[0]] = n[1],this}
    .bind({}))[0];
  }
  return null;
},//query params

  //generic ajax post requires the action endpoint and data as a javascript object.
  this.postem = function(endpoint, payload) {
    return new Promise(function(resolve, reject){
      $.ajax({
        url: endpoint,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(payload),
        success: function(data) {
          resolve(data);
        },
        error: function(err){
          resolve(err);
        }
      })
    })
  },//postem

  //convert form elements into a js object
  this.getFormElements = function() {
    var Formy = this;
    var elements = document.getElementById(Formy.form.attr('id')).elements;
    var data = {};

     for (var i=0; i<elements.length; i++) {
       if(elements[i].value && elements[i].value !== "") {
         data[elements[i].name] = elements[i].value;
       } else if (elements[i].checked) {
         data[elements[i].name] = true;
       }
     }
     return data;
   }//getFormElements
}//Formy

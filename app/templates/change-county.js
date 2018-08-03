function disableSubmitBtn() {
  let btn = $('#btn-next');
  if (!btn.data('enabled')) {
    btn.data('enabled', btn.text());
  }
  btn.text(btn.data('disabled'));
  btn.prop('disabled', true);
}
function enableSubmitBtn() {
  let btn = $('#btn-next');
  btn.text(btn.data('enabled'));
  btn.prop('disabled', false);
}

$('#change-county-btn').click(function(ev) {
  $('#change-county-picker').toggle();
  let tag = $(this);
  // TODO toggle tag text?

  // animated scroll to picker
  let scrollTarget = tag.attr('href');
  $([document.documentElement, document.body]).animate({
    scrollTop: $(scrollTarget).offset().top - 60
  }, 500);

  // disable main Submit button if we have un-applied changes.
  if ($('#change-county-picker').is(':hidden')) {
    enableSubmitBtn();
  }
  else {
    disableSubmitBtn();
  }
});

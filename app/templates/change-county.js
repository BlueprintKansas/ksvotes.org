function disableSubmitBtn() {
  let btn = $('{{next_btn_selector or '#btn-next'}}');
  if (!btn.data('enabled')) {
    btn.data('enabled', btn.text());
  }
  btn.text(btn.data('disabled'));
  btn.prop('disabled', true);
}
function enableSubmitBtn() {
  let btn = $('{{next_btn_selector or '#btn-next'}}');
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

// MUST have a county selected to proceed
// In theory we should never get here, but belt-and-suspenders ftw.
$('{{next_btn_selector or '#btn-next'}}').click(function(ev) {
  let county = $('.clerk-details .county').text();
  let error_msg = $('#county-error');
  error_msg.hide(); // always clear to start with.
  if (!county.length) {
    error_msg.show();
    ev.preventDefault();
    return false;
  }
  return true;
});

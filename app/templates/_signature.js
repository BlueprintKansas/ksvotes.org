<script src="{{url_for('static', filename='js/jSignature.min.js')}}"></script>
<script>
    $(document).ready(function() {
        $("#signature").jSignature({
          'background-color': '#ffffff',
          'decor-color': 'transparent',
        });

        // fill the space as CSS dictates
        let sig_canvas = $('#signature canvas')[0];
        sig_canvas.width = $('#signature-wrapper').width();
        sig_canvas.height = $('#signature-wrapper').height();
        sig_canvas.style.width = '100%';
        sig_canvas.style.height = '100%';

        // pre-fill if defined
        $sig_string = $('#signature_string');
        if ($sig_string.val().length > 0) {
          $('#signature').jSignature('setData', $sig_string.val());
        }
        // "normal" required field validation doesn't work because signature_string is hidden
        $('#sign-button').click(function(ev) {
          $('.parsley-errors-list').empty();
          if ($('#signature_string').val().length == 0) {
            ev.preventDefault();
            $('.parsley-errors-list').append($('<li>Signature required</li>'));
          }
        });
    })
    $("#signature").bind('change', function(e){
      if( $('#signature').jSignature('getData', 'native').length == 0) {
         return;
      } else {
        $('#signature_string').val($('#signature').jSignature('getData'));
      }
    });
    var resetHiddenSignatureImg = function() {
      $('#signature').jSignature('reset');
      $('#signature_string').val('');
      return false; // abort onclick handler
    };
</script>

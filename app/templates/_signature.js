<script src="{{url_for('static', filename='js/signature_pad.min.js')}}"></script>
<script>
    $(document).ready(function() {
      // add canvas element
      let $signature = $("#signature");
      let $sig_string = $('#signature_string');
      $signature.append('<canvas></canvas>');
      let canvas = $signature.find('canvas')[0];
      let sig_pad = new SignaturePad(canvas, {
        onEnd: function() {
          let sig_png = sig_pad.toDataURL();
          if (sig_png.length == 0) {      
          } else {
            $sig_string.val(sig_png);
          }
        }
      });

      function fillCanvasFromPNG() {
        if ($sig_string.val().length > 0) {
          sig_pad.fromDataURL($sig_string.val());
        }
      }

      // Adjust canvas coordinate space taking into account pixel ratio,
      // to make it look crisp on mobile devices.
      // This also causes canvas to be cleared.
      function resizeCanvas() {
        // When zoomed out to less than 100%, for some very strange reason,
        // some browsers report devicePixelRatio as less than 1
        // and only part of the canvas is cleared then.
        let ratio =  Math.max(window.devicePixelRatio || 1, 1);

        // This part causes the canvas to be cleared
        canvas.width = canvas.offsetWidth * ratio;
        canvas.height = canvas.offsetHeight * ratio;
        canvas.getContext("2d").scale(ratio, ratio);

        // This library does not listen for canvas changes, so after the canvas is automatically
        // cleared by the browser, SignaturePad#isEmpty might still return false, even though the
        // canvas looks empty, because the internal data of this library wasn't cleared. To make sure
        // that the state of this library is consistent with visual state of the canvas, you
        // have to clear it manually.
        sig_pad.clear();
        fillCanvasFromPNG();
      }

      window.onresize = resizeCanvas;
      window.orientationchange = resizeCanvas;
      resizeCanvas(); // set initial size and existing signature

      // "normal" required field validation doesn't work because signature_string is hidden
      $('#sign-button').click(function(ev) {
        $('.parsley-errors-list').empty();
        if ($sig_string.val().length == 0) {
          ev.preventDefault();
          $('.parsley-errors-list').append($('<li>Signature required</li>'));
        }
      });

      $('#btn-clear-signature').on('click', function(ev) {
        ev.preventDefault(); // do not submit (multiple buttons confuse browser)
        sig_pad.clear();
        $('#signature_string').val('');
      });
    });
</script>

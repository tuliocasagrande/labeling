function displayHeader(header) {
  var $label_name = $("#label_name");
  $label_name.html("");
  header.forEach(function(record) {
    option = '<option value="'+record+'">'+record+'</option>';
    $label_name.prepend(option);
  });
}

$(function(){
  $("#dataset").change(function(){
    $(this).parse({
      config: {
        complete: function(results, file) {
          displayHeader(results.data[0]);
        }
      }
    });
  });

  $("#append_label_column").change(function() {
    if ($(this).is(":checked")) {
      $("#label_name_row").fadeOut(function() {
        $("#label_name").prop('disabled', true);
      });
    } else {
      $("#label_name").prop('disabled', false);
      $("#label_name_row").fadeIn();
    }
  });

  // Just in case the user clicks the browser's back button
  $("#dataset").change();
  $("#append_label_column").change();
});

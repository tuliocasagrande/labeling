function readDataset(file) {
  if (!file) {
    return;
  }
  var reader = new FileReader();
  reader.onload = function(e) {
    var contents = e.target.result;
    displayHeader(contents);
  };
  reader.readAsText(file);
}

function displayHeader(contents) {
  var header = new CSV(contents).parse()[0];
  var $label_column_name = $("#label-column-name");
  $label_column_name.html("");
  header.forEach(function(record) {
    option = '<option value="'+record+'">'+record+'</option>';
    $label_column_name.prepend(option);
  });
}

$(function(){
  $("#dataset").change(function(){
    var file = this.files[0];
    readDataset(file);
  });
  // Just in case the user clicks the browser's back button
  $("#dataset").change();

  $("#has-header").change(function() {
    if ($(this).is(":checked")) {
      $("#label-column-name").prop('disabled', false);
    } else {
      $("#label-column-name").prop('disabled', true);
    }
  });
});


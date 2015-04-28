$(function(){

  function readSingleFile(e) {
    var file = e.target.files[0];
    if (!file) {
      return;
    }
    var reader = new FileReader();
    reader.onload = function(e) {
      var contents = e.target.result;
      displayContents(contents);
    };
    reader.readAsText(file);
  }

  function displayContents(contents) {
    var element = document.getElementById("select-class");
    element.innerHTML = contents.substring(0, contents.indexOf("\n"));

    var header = new CSV(contents).parse()[0];

    element.innerHTML = '';
    header.forEach(function(record) {
      option = '<option value="'+record+'">'+record+'</option>';
      element.innerHTML = option + element.innerHTML;
    });
  }

  document.getElementById("dataset")
    .addEventListener("change", readSingleFile, false);
});


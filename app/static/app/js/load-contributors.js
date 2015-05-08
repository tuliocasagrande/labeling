
var contributors = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: '/users/search/%QUERY',
    wildcard: '%QUERY'
  }
});

$('#typeahead_contributor .typeahead').typeahead({
  highlight: true,
  minLength: 2
},
{
  name: 'contributors',
  limit: 5,
  display: 'value',
  source: contributors
});

$('#add_contributor').submit(function(e){
  e.preventDefault();

  var $contributor = $('#contributor');
  if (!$contributor.val()){
    return;
  }

  $.ajax({
    method: 'POST',
    url: $(this).attr('action'),
    headers: {'X-CSRFToken': $.cookie('csrftoken') },
    data: {contributor: $contributor.val() }
  })
  .fail(function(data) {
    console.log(data.responseText);
  })
  .done(function( data ) {
    $('#contributors').append('<p>'+$contributor.val()+'</p>')
    $contributor.val('');
  });
});

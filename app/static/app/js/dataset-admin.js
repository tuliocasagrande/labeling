$(function(){
  $('[data-toggle="tooltip"]').tooltip();

  var contributors = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
      url: $('#logo_index').attr('href') + 'users/search/%QUERY',
      wildcard: '%QUERY'
    }
  });

  $('#contributor_input').typeahead({
    hint: true,
    highlight: true,
    minLength: 2
  },
  {
    name: 'contributors',
    display: 'value',
    source: contributors
  });

  $('#add_contributor').submit(function(e){
    e.preventDefault();

    var $contributor = $('#contributor_input');
    if (!$contributor.val()){
      return;
    }
    var url = $(this).attr('action');

    $.ajax({
      method: 'POST',
      url: $(this).attr('action'),
      headers: {'X-CSRFToken': $.cookie('csrftoken') },
      data: {contributor: $contributor.val() }
    })
    .fail(function(data) {
      console.log(data.responseText);
    })
    .done(function() {
      var row = '<tr><td>'+$contributor.val()+'</td><td>' +
            '<a href="'+url + $contributor.val()+'/" class="remove_contributor" rel="nofollow">' +
            '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>' +
            '</a></td></tr>';
      $('#contributors').append(row);
      $contributor.val('');
    });
  });

  $('#contributors').on('click', '.remove_contributor', function(e) {
    e.preventDefault();

    var $contributor_row = $(this).parent().parent();

    $.ajax({
      method: 'DELETE',
      url: $(this).attr('href'),
      headers: {'X-CSRFToken': $.cookie('csrftoken') }
    })
    .fail(function(data) {
      console.log(data.responseText);
    })
    .done(function() {
      $contributor_row.fadeOut(function() { $(this).remove(); });
    });
  });


  $('#delete_dataset').click(function(e) {
    $.ajax({
      method: 'DELETE',
      url: $(this).attr('href'),
      headers: {'X-CSRFToken': $.cookie('csrftoken') }
    })
    .fail(function(data) {
      console.log(data.responseText);
    })
    .done(function(data) {
      window.location.href = data.redirect;
    });
  });
});

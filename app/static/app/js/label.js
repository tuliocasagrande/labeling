$(function () {
  $('[data-toggle="tooltip"]').tooltip();

  $('.hide-column').click(function() {
    var column = $(this).attr('data-column');
    $('.' + column).fadeOut(500);
    $('#' + column + '-btn').fadeIn(500);
  });

  $('.show-column').click(function() {
    var column = $(this).attr('data-column');
    $('.' + column).fadeIn(500);
    $('#' + column + '-btn').fadeOut(500);
  });

  $('#more_labels').click(function() {
    $.ajax({
      method: 'GET',
      url: window.location,
      headers: {'X-CSRFToken': $.cookie('csrftoken') },
    })
    .fail(function(data) {
      console.log(data.responseText);
    })
    .done(function(data) {
      console.log(data);
    });
  });
});

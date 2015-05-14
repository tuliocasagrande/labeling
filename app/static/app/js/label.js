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

  $('.label-btn').click(function() {
    var $this = $(this);
    var label = $this.attr('data-label');
    var sample_id = $this.parent().attr('data-sample-id');

    $this.removeClass('btn-default').addClass($this.attr('btn-color'));
    $this.siblings().removeClass('btn-danger btn-warning btn-success btn-primary').addClass('btn-default');


    $.ajax({
      method: 'POST',
      url: window.location,
      headers: {'X-CSRFToken': $.cookie('csrftoken') },
      data: {'label': label, 'sample_id': sample_id}
    })
    .fail(function(data) {
      console.log(data.responseText);
    })
    .done(function(data) {
      console.log(data);
    });
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

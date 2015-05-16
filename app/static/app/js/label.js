function hideColumn(column, update_url) {
  update_url = typeof update_url !== 'undefined' ? update_url : true;
  $('#table-column-' + column + '-btn').fadeIn();
  $('.table-column-' + column).fadeOut().promise().done(function() {
    if (update_url) updateUrl();
  });
}

function showColumn(column) {
  $('#table-column-' + column + '-btn').fadeOut();
  $('.table-column-' + column).fadeIn().promise().done(function() {
    updateUrl();
  });
}

function updateUrl() {
  var $visible_columns = $('.show-column:visible');
  var total = $visible_columns.length;
  if (total === 0) {
    window.history.replaceState({}, '', location.pathname);
  } else {
    var url = '?hidden-columns=';
    $visible_columns.each(function(index) {
      url += $(this).attr('data-column');
      if (index !== total - 1) {
        url += ',';
      }
    });
    window.history.replaceState({}, '', url);
  }
}

function parseURI(val) {
  var result = '', tmp = [];
  location.search.substr(1).split("&").forEach(function(item) {
    tmp = item.split("=");
    if (tmp[0] === val) result = decodeURIComponent(tmp[1]);
  });
  return result;
}

$(function () {
  parseURI('hidden-columns').split(',').forEach(function(item) {
    hideColumn(item, false);
  });

  $('#body-container').removeClass('container').addClass('container-fluid');

  $('[data-toggle="tooltip"]').tooltip();

  $('.hide-column').click(function() {
    hideColumn($(this).attr('data-column'));
  });

  $('.show-column').click(function() {
    showColumn($(this).attr('data-column'));
  });

  $('#samples_tbody').on('click', '.label-btn', function(e) {
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
      $this.parent().parent().fadeOut();
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
      $('#samples_tbody').append(data);
      parseURI('hidden-columns').split(',').forEach(function(item) {
        hideColumn(item, false);
      });
      console.log(data);
    });
  });
});

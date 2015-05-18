function hideColumn(column, animate) {
  animate = typeof animate !== 'undefined' ? animate : true;
  $('#table-column-' + column + '-btn').fadeIn().addClass('visible-column');
  if (animate) {
    $('.table-column-' + column).fadeOut();
    updateUrl();
  } else {
    $('.table-column-' + column).fadeOut(0);
  }
}

function showColumn(column) {
  $('#table-column-' + column + '-btn').fadeOut().removeClass('visible-column');
  $('.table-column-' + column).fadeIn();
  updateUrl();
}

function updateUrl() {
  var $visible_columns = $('.visible-column');
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

function loadSamples() {
  parseURI('hidden-columns').split(',').forEach(function(item) {
    hideColumn(item, false);
  });
  $('.unlabeled-sample').removeClass('hidden');
}

function moreSamples() {
  $.ajax({
    method: 'GET',
    url: window.location,
    headers: {'X-CSRFToken': $.cookie('csrftoken') },
  })
  .fail(function(data) {
    console.log(data.responseText);
  })
  .done(function(data) {
    if (data === 'done!') {
      $('#done_labeling').removeClass('hidden');
      $('#labeling-wrapper').remove();
    } else {
      $('#samples_tbody').append(data);
      loadSamples();
    }
  });
}

$(function () {
  $('#body-container').removeClass('container').addClass('container-fluid');
  $('[data-toggle="tooltip"]').tooltip();
  loadSamples();

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
      $this.parent().parent().fadeOut().removeClass('unlabeled-sample');
      if ($('.unlabeled-sample').length === 0) moreSamples();
    });
  });

});

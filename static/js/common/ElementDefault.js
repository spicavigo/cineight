$(function() {
 /*   
  $('#UIDialog').dialog({
    autoOpen: false
    });
*/

  $('.has_data_id').live("click", function() {
    var that = this;
    $.get(AJAX_URL, {
      'data_id': $(that).attr("data-id")
      }, function(html) {
      $('#UIDialog').html(html);
      $('#UIDialog').dialog('open');
      });
    });
  $('.shareBtns button').click(function() {
    var that = this;
    $.get(AJAX_URL, {
      'data_id': $(that).attr("data-id")
      }, function(response) {
      });
    });
  });


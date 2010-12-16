
$(document).ready(function() {
  $('.rollover').each(function() {
    var currentImage = $(this).attr("src");
    var rolloverImg = new Image();
    rolloverImg.src = $(this).attr("data-rollover");
    $(this).data("rollover_image", rolloverImg);
    $(this).data("orig_image", currentImage);
    $(this).hover(function() {
      if ($(this).parent().hasClass('iconSelected') || $(this).parent().hasClass('univSelected')) {
        return;
      }
      $(this).attr("src", $(this).attr("data-rollover"));
      }, function() {
      if ($(this).parent().hasClass('iconSelected') || $(this).parent().hasClass('univSelected')) {
        return;
      }
      $(this).attr("src", $(this).data("orig_image"));
    });
  });

});


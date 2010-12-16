$(function() {
    $('.signup_form').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(response){
            if (response.success){
                window.location = response.url;
            } else {
                $('.signup_error').html(response.error);
                $('.signup_error').show();
            }
       });
       
    });
    
});


$(function() {
    $('.login_form').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(response){
            if (response.success){
                window.location = response.url;
            } else {
                $('.login_error').html(response.error);
                $('.login_error').show();
            }
       });       
    });    
});


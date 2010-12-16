$(function() {
    
    $('.reco_form_form').hide();
    $('.show_reco').live('click', function(){
        $(this).siblings('.reco_form_form').toggle('slow');
    });
    $('.reco_form_form').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(html){
       });
       $(this).hide('slide');
    });
    
    $('.list').live('click', function(){
        var data_id = $(this).attr('data-id');
        $(this).toggleClass('selected');
        $.get(AJAX_URL, {'data_id': data_id}, function(html){});
        if ($(this).hasClass('mutex')){
            if($(this).hasClass('selected')){
                $(this).siblings('.mutex').each(function(){
                    $(this).removeClass('selected');
                    });
            }
        }
    });
});


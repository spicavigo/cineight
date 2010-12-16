$(function() {
    $('.rating').rating({'showCancel':false});
    $('.reco_form_movie').hide();
    $('.warn_form_movie').hide();
    //$('.reco_form_movie').show();
    $('.show_reco').live('click', function(){
        $(this).siblings('.reco_form_form').toggle('slow');
    });
    $('.reco_form_movie').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(html){
            $('.TabReview').replaceWith(html);
       });
       $(this).hide('slide');
    });
    $('.warn_form_movie').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(html){
            $('.TabReview').replaceWith(html);
       });
       $(this).hide('slide');
    })
    $('.reco_action').live('click', function(){
        var form_acted = $(this).siblings('.reco_form_movie');
        $('.warn_form_movie').hide('slide');
        $('.reco_form_movie').not(form_acted).hide()
        $(form_acted).toggle('slide');
        
    });
    
    $('.warn_action').live('click', function(){
        var form_acted = $(this).siblings('.warn_form_movie')
        $('.reco_form_movie').hide('slide');
        $('.warn_form_movie').not(form_acted).hide()
        $(form_acted).toggle('slide');
        
    });
});
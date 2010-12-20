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
       if(window.parent.location !=  window.location){
        var movie_name = $.trim($(this).parents('.reco_left').find('.reco_mname').html());
        var movie_year = $.trim($(this).parents('.reco_left').find('.reco_myear').html());
        var comment = $(this).find('[name=comment]').val();
        var rating = $(this).find('[name=rating]').val();
        publishRec(movie_name + '(' + movie_year + '): ' + comment + '(+' + rating + '/5)' );
       }
    });
    $('.warn_form_movie').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(html){
            $('.TabReview').replaceWith(html);
       });
       $(this).hide('slide');
       if(window.parent.location !=  window.location){
        var movie_name = $.trim($(this).parents('.reco_left').find('.reco_mname').html());
        var movie_year = $.trim($(this).parents('.reco_left').find('.reco_myear').html());
        var comment = $(this).find('[name=comment]').val();
        var rating = $(this).find('[name=rating]').val();
        publishRec(movie_name + ' ' + movie_year + ': ' + comment + '(-' + rating + '/5)' );
        }
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
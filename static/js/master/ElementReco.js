$(function() {
    function alternate(div){
        $(div).find('>:odd').removeClass('elementEven').removeClass('elementOdd').addClass('elementOdd');
        $(div).find('>:even').removeClass('elementOdd').removeClass('elementEven').addClass('elementEven');
    }
    $('.rating').rating({'showCancel':false});
    $(".delete_reco").tipTip({edgeOffset:10});
    $('.delete_reco').live('click', function(){
        var data = $(this).attr('data-id');
        var that = this;
        $.get(AJAX_URL, {'data_id': data}, function(html){
            if (html.success){
                var tab = $(that).parents('.lzTab');
                $(that).parents('.elementEven').remove();
                $(that).parents('.elementOdd').remove();
                alternate($(tab).find('.elements'));
            }
        });
    });
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
        if (movie_name == "" && movie_year == ""){
            movie_name = $.trim($('.movie_mname').html());
            movie_year = $.trim($('.movie_myear').html());
        }
        var comment = $(this).find('[name=comment]').val();
        var rating = $(this).find('[name=rating]').val();
        publishRec(movie_name +  movie_year + ': ' + comment + '(+' + rating + '/5)' );
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
        if (movie_name == "" && movie_year == ""){
            movie_name = $.trim($('.movie_mname').html());
            movie_year = $.trim($('.movie_myear').html());
        }
        var comment = $(this).find('[name=comment]').val();
        var rating = $(this).find('[name=rating]').val();
        publishRec(movie_name + ' ' + movie_year + ': ' + comment + '(-' + rating + '/5)' );
        }
    })
    $('.reco_action').live('click', function(){
        /*var form_acted = $(this).siblings('.reco_form_movie');
        $('.reco_form_movie').not(form_acted).hide('fast');
        $('.warn_form_movie').hide('fast');
        $(form_acted).toggle('slow');*/
        $(this).parents('.reco_form').children().removeClass('r_selected');
        $(this).addClass('r_selected');
        var data_id = $(this).attr('data-id');
        $.get(AJAX_URL, {data_id: data_id}, function(){});
    });
    
    $('.warn_action').live('click', function(){
        /*var form_acted = $(this).siblings('.warn_form_movie');
        $('.warn_form_movie').not(form_acted).hide('fast');
        $('.reco_form_movie').hide('fast');
        $(form_acted).toggle('slow');*/
        var data_id = $(this).attr('data-id');
        $(this).parents('.reco_form').children().removeClass('r_selected');
        $(this).addClass('r_selected');
        
        $.get(AJAX_URL, {data_id: data_id}, function(){});
    });
    
    $('.rating').bind('change', function(){
        var value = $(this).val();
        $(this).siblings('.rate_text').children('span').html(' ' + value + '/10');
        var data_id = $(this).attr('data-id');
        $.get(AJAX_URL, {data_id: data_id, rating: value}, function(){});
        
    })
});
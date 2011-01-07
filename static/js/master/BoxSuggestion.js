$(function(){
    $('ul.suggest_tab_title li a').live('click', function(){
        var id = $(this).attr('href');
        $('.suggest_content').fadeOut('fast', function(){
            $('.suggest_content').html($(id).html());
            $('.suggest_content').fadeIn('slow');
            });
        
        $(this).parents('ul').children('li').removeClass('active');
        $(this).parent('li').addClass('active');
        });
});

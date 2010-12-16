

$(document).ready(function() {    
    $('#purgelist').live('click', function(){
        var that=this;
        $('.compare_list').removeClass('selected');
        $.get(AJAX_URL, {
                        'data_id': $(that).attr("data-id")
                        },
                        function(response){
                            $.fancybox.close();
                        });
    });	
}); 
	
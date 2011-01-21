$(function() {
    var AC = $('#main-query').autocomplete({ 
        serviceUrl:AJAX_URL,
        minChars:2, 
        //delimiter: /(,|;)\s*/, // regex or character
        maxHeight:400,
        width:300,
        zIndex: 9999,
        deferRequestBy: 0, //miliseconds
        params: { data_id: $('.search_movie').attr('data-id') }, //aditional parameters
        noCache: false, //default is false, set to true to disable caching
        // callback function:
        onSelect: function(value, data){ window.location = 'http://' + window.location.host + '/movie/' + data }
    });
    $('#main-query').focus(function(){
        var that = $(this);
        if (that.val() == 'Search for User or Input...'){
            that.val('');
            that.removeClass('italic light');
            AC.enable();
        }
    });
    $('#main-query').blur(function(){
        var that = $(this);
        if (that.val() == ''){
            AC.disable();
            $('#main-query').addClass('italic light');
            that.val('Search for User or Input...');
        }
    });
    if($('#main-query').val() == '' || $('#main-query').val() == 'Search for User or Input...' ){
        AC.disable();
        $('#main-query').addClass('italic light');
        $('#main-query').val('Search for User or Input...');
    }
});
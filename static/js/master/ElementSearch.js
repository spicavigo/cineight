$(function() {
    $('#main-query').autocomplete({ 
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
        onSelect: function(value, data){ window.location = 'http://' + window.location.host + '/movie/' + data },

  });
});
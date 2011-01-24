    //function for the navigation button
$(function(){
    function elementInViewport2(el) {
        var top = el.offsetTop;
        var left = el.offsetLeft;
        var width = el.offsetWidth;
        var height = el.offsetHeight;
      
        while(el.offsetParent) {
          el = el.offsetParent;
          top += el.offsetTop;
          left += el.offsetLeft;
        }
      
        return (
          top < (window.pageYOffset + window.innerHeight) &&
          left < (window.pageXOffset + window.innerWidth) &&
          (top + height) > window.pageYOffset &&
          (left + width) > window.pageXOffset
        );
    }
    
    var clicked = false;
    function getNext(e){
        if (clicked) {
            return false;
        }
        clicked = true;
        var that = this;
        var data_id = $(this).attr("data-id");
        var len = $(that).parents('.lzTab').find('.elements > div').length - 1;
        $(this).html("");
        $(this).css({'background':'url("/static/images/loading_bar.gif") no-repeat center center',
                    'border': 'none'});
        $.get(AJAX_URL, {
            'data_id': data_id
        }, function(html) {
            var parent = $(that).parents('.lzTab');
            $(html).find("span.spoiler").hide();
            var is_grid = parent.find('.togrid').hasClass('selected');
            parent.find('.elements').append($(html).find('.elements').html());
            $('.rating:not("#ui-rating-null")').rating({'showCancel':false});            
            clicked = false;
            var new_parent = parent.find('.elements > div:gt(' + len + ')');
            init_textarea(new_parent);
            new_parent.find('textarea').autoResize(); 
            /*new_parent.find('.mimage').appear(function(){
                var that = $(this);
                $(this).attr('src', that.attr('data-src'));
              }, {
                one: true
            });*/
            if (is_grid){
                new_parent.find('.mimage').each(function(){
                    $(this).after('<div class="img_title">' + $(this).attr('alt').substr(0, 30) +'</div>');
                    $(this).qtip({
                        content: { text: $(this).parents('.reco_element').html() },
                        show: {
                            when: 'mouseover',
                            solo: true
                        },
                        hide: {
                            fixed: true
                        },
                        style: {
                            width: 420,
                            background: '#F6F6F6',
                            border: {
                                width: 1,
                                radius: 3,
                                color: '#3F4C6B'
                            }
                        },
                        position: {
                            target: 'mouse',                            
                            viewport: $(window),
                            adjust: { screen: true, mouse: false }
                        }
                    });
                });
            }
            FB.XFBML.parse();
            parent.find('.tabBtns').replaceWith($(html).find('.tabBtns'));
            parent.find('.tabNav').appear(getNext, {one: true});
        });
    }
    $('.tabNav').live("click", getNext);
    $('.tabNav').appear(getNext, {one: true});
    $('.tolist').live('click', function(){
        if ($(this).hasClass('selected')){
            return false;
        }
        $(this).addClass('selected');
        $(this).parent().find('.togrid').removeClass('selected');
        var elems = $(this).parents('.tab_content').find('.elements');
        elems.removeClass('grid');
        elems.find('.img_title').remove();
        elems.find('.mimage').each(function(){
            $(this).qtip('destroy');
        });
    });
    $('.togrid').live('click', function(){
        if ($(this).hasClass('selected')){
            return false;
        }
        $(this).addClass('selected');
        $(this).parent().find('.tolist').removeClass('selected');
        var elems = $(this).parents('.tab_content').find('.elements');
        elems.addClass('grid');
        elems.find('.mimage').each(function(){
            $(this).after('<div class="img_title">' + $(this).attr('alt').substr(0, 30) +'</div>');
            $(this).qtip({
                content: { text: $(this).parents('.reco_element').html() },
                show: {
                    when: 'mouseover',
                    solo: true
                },
                hide: {
                    fixed: true
                },
                style: {
                    width: 420,
                    background: '#F6F6F6',
                    border: {
                        width: 1,
                        radius: 3,
                        color: '#3F4C6B'
                    }
                },
                api: {
                    onRender: function(){this.elements.tooltip.draggable();this.elements.tooltip.find('textarea').autoResize();init_textarea(this.elements.tooltip);}
                },
                position: {
                    target: 'mouse',                    
                    viewport: $(window),
                    adjust: { screen: true, mouse: false }
                }
            });
        });
    });
});


$(document).ready(function() {

  function alternate(div){
    $(div).find('>:odd').removeClass('elementEven').removeClass('elementOdd').addClass('elementOdd');
    $(div).find('>:even').removeClass('elementOdd').removeClass('elementEven').addClass('elementEven');
  }
    //Orbited.settings.port = 9000;
    //Orbited.settings.hostname = "localhost";
    var lzOrbited = function() { 
      var that = this;
      var TCPSocket = Orbited.TCPSocket;
          
      this.conn = new TCPSocket();
      
      this.conn.onopen = function() { that.conn.send(USER+'\r\n'); };
      this.conn.onread = function(data) { 
        var json = JSON.parse(data);
        var key = json.action;        
        that.onreadCallback[key](json);
        };

      this.conn.onclose = function(data) { }
      this.conn.open("localhost", 7778);
      this.onreadCallback = {
        'ADD': function(json){
            $('#'+json.tab).find('.elements').prepend('<div>' + json.html + '</div>');
            $('#'+json.tab).find('.RAEmpty').remove();
            alternate($('#'+json.tab).find('.elements'));
            $('#'+json.tab).find('[data-id='+json.id+']').find('.rating').rating({'showCancel':false});
            if (json.mid){
              var lists = $('.reco_right > [data-id='+json.mid+']');
               lists.find('.mutex').removeClass('selected');
               lists.find('.list_'+json.tab).addClass('selected');
            }
          },
        'DEL': function(json){
          $('#'+json.tab).find('div[data-id="' + json.id +'"]').parent().fadeOut(500, function(){
                                                                                  $(this).remove();
                                                                                  alternate($('#'+json.tab).find('.elements'));
                                                                                 });
          
        }
        };
      };
    window.lzComet = new lzOrbited();          
    });



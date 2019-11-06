$(function() {
    $.ajax({
        url: "{{ url_for('room.song_autocomplete') }}"
        }).done(function (data) {
            var options = data.options
            if(typeof options !== "undefined") {
                $('#autocomplete').autocomplete({
                    source: data.options,
                    minLength: 2
                });
            }
        });
    });

$(function() {
$('#autocomplete').autocomplete({
    source: function( request, response ) {
        $.ajax( {
          url: "{{ url_for('room.song_autocomplete') }}"+"?term="+request.term,
          dataType: "jsonp",
          success: function( data ) {
            response( data );
          }
        } );
        },
    minLength: 2
    });
});

 $( "#birds" ).autocomplete({
      source: function( request, response ) {
        $.ajax( {
          url: "search.php",
          dataType: "jsonp",
          data: {
            term: request.term
          },
          success: function( data ) {
            response( data );
          }
        } );
      },
      minLength: 2,
      select: function( event, ui ) {
        log( "Selected: " + ui.item.value + " aka " + ui.item.id );
      }
    } );
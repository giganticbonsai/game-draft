var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/room');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    socket.on('status', function(data) {
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('guess', function(data) {
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('update', function(data) {
        $('#time').html(data.time);
        $('#song').html(data.song)
        var guesses = data.guesses
        latest_guesses = '';
        for (var i = 0; i < guesses.length; i++){
            latest_guesses = latest_guesses + '<li class="list-group-item">' + guesses[i] + '</li>';
        }
        $('#latest_guesses').html(latest_guesses);
        var clues = data.clues
        clue_values = '';
        for (var key in clues) {
            if (clues.hasOwnProperty(key)) {
            img = '<img src="'+ clues[key]['image'] +
            '" class="bd-placeholder-img card-img-top" width="140" height="140" alt="Clue" class="img-circle">'
            clue_values = clue_values +
            '<div class="col-sm-4 col-md-offset-1"><div class="card mb-4 shadow-sm">' + img + '<div class="card-body"><h5 class="card-title text-center">'+
             clues[key]['value'] +'</h5></div></div></div>';
            }
        }
        $('#clues').html(clue_values);
    });
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('guess', {msg: text});
        }
    });
});
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('main.index') }}";
    });
}
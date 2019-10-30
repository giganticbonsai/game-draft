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
        var guesses = data.guesses
        latest_guesses = '';
        for (var i = 0; i < guesses.length; i++){
            latest_guesses = latest_guesses + '<p>' + guesses[i] + '</p>';
        }
        $('#latest_guesses').html(latest_guesses);
    });
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('guess', {msg: text});
        }
    });
    socket.on('openClue', function(data) {
        $('#'+data.clue).text(data.value);
    });
});
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('main.index') }}";
    });
}
function open_clue() {
    socket.emit('open_clue', {});
}
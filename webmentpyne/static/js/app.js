function get_status() {
    $.ajax({url:'/player/',
        success:function (data, textStatus, jqXHR) {
            if (data.status) {
                $('#controls').show();
                $('#statusbar').show();
                $('#current').html(data.response.html);
                $('#status').html('player is: ' + data.response.PlaybackStatus.toLowerCase());
                $('#shuffle').html('shuffle: ' + (data.response.Shuffle ? 'yes' : 'no'));
                $('#repeat').html('repeat: ' + data.response.LoopStatus.toLowerCase());
                $('#volume').html('volume: ' + data.response.Volume.toPrecision(3) * 100 + '%');
            }
            else {
                $('#current').load('connection-error');
                $('#controls').hide();
                $('#statusbar').hide();
            }
        }})
}

$(document).ready(function () {
    $('#controls button').click(function () {
        $.get('/player/' + this.id,function (data, textStatus, jqXHR) {
            get_status();
        }).error(function () {
                alert('It seems that player or webserver is not running.')
            });
    });

    $('#remote-form').submit(function () {
        $.get('/player/OpenUri/' + $('#remote').val(),function (data, textStatus, jqXHR) {
            get_status();
        }).error(function () {
                alert('It seems that player or webserver is not running.')
            });
    });

    get_status();
    setInterval(get_status, 5000);

});


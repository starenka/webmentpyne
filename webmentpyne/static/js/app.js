(function worker() {
    $.ajax({url:'/player/',
        success:function (data, textStatus, jqXHR) {
            if (data.status) {
                $('#controls').show();
                $('#current').html(data.response.html);
            }
            else {
                $('#current').load('connection-error');
                $('#controls').hide();
            }
        },
        complete:function () {
            setTimeout(worker, 5000);
        }})
})();


$(document).ready(function () {
    $('#controls button').click(function () {
        $.get('/player/' + this.id,function (data, textStatus, jqXHR) {
        }).error(function () {
                alert('It seems that Clementine or webserver is not running.')
            });
    });

});


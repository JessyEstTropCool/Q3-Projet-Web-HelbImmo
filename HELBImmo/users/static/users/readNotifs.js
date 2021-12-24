//requests for all unread notifications to be read
$(document).ready(function () {
    $(".js-read").each(function () {
        let info = $(this);
        $.ajax({
            url: info.attr('read-url'),
            data: {
                'notifid': info.attr('data-notifid')
            }
        });
    });
});
//adds a view to post on load
$(document).ready(function () 
{
    let info = $(".js-view").first();
    $.ajax({
        url: info.attr('view-url'),
        data: {
            'postid': info.attr('data-postid')
        },
        success: function (result) 
        {
            console.log(result.good);
        }
    }); 
});
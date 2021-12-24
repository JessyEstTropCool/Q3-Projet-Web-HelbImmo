$(document).ready(function () {
    //activates tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    //enables buttons with .js-fav class to add/remove favorites and change posts accordingly
    $(".js-fav").click(function () {
        let btn = $(this);
        let postid = $(this).data('postid');
        console.log("fav " + postid + "!");
        $.ajax({
            url: btn.attr('fav-url'),
            data: {
                'postid': postid
            },
            success: function (result) {
                if (result.added === true) {
                    btn.children().first().removeClass("bi-star").addClass("bi-star-fill");
                    btn.children().last().text("Dans les favoris");
                }
                else {
                    btn.children().first().removeClass("bi-star-fill").addClass("bi-star");
                    btn.children().last().text("Ajouter aux favoris");
                }
            }
        });
    });

    //adds any GET request parameters to href url (for pagination)
    $('.js-get').each(function (compt, elem) {
        let key = elem.getAttribute('data-key');
        let value = elem.getAttribute('data-value');

        if (key != null && value != null) {
            let searchParams = new URLSearchParams(window.location.search);
            searchParams.set(key, value);

            elem.setAttribute('href', '?' + searchParams);
        }
    });

    //removes any unused fields while using searchbar
    $('#searchform').submit(function () {
        $(this)
            .find('input[name]')
            .filter(function () {
                return !this.value && this.name != "q";
            })
            .prop('name', '');
    });
});
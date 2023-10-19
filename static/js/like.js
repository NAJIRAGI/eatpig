$('.favorite').click(function (event) {
    let favorite_id = event.target.id;
    let favorite_text = $.trim($('#' + favorite_id).html());
    let feed_id = event.target.attributes.getNamedItem('data-feed_id').value;

    if (favorite_text == 'favorite') {
        $('#' + favorite_id).html('favorite_border');
    } else {
        $('#' + favorite_id).html('favorite');
    }

    $.ajax({
        url: "/contents/like/",
        data: {
            feed_id: feed_id,
            favorite_text: favorite_text
        },
        method: "POST",
        success: function (data){
            console.log("성공");
            location.reload();
        },
        error: function () {
            console.log("에러");
        },
        complete: function () {
            console.log("완료");
        }
    });

});
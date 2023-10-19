$('.bookmark').click(function (event) {
    let bookmark_id = event.target.id;
    let bookmark_text = $.trim($('#' + bookmark_id).html());
    let feed_id = event.target.attributes.getNamedItem('data-feed_id').value;

    console.log(bookmark_text)
    console.log(bookmark_id)

    if (bookmark_text == 'bookmark') {
        $('#' + bookmark_id).html('bookmark_border');
    } else {
        $('#' + bookmark_id).html('bookmark');
    }

    $.ajax({
        url: "/contents/bookmark/",
        data: {
            feed_id: feed_id,
            bookmark_text: bookmark_text
        },
        method: "POST",
        success: function (data){
            console.log("성공");
        },
        error: function () {
            console.log("에러");
        },
        complete: function () {
            console.log("완료");
        }
    });

});
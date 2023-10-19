$('.reply_send').click(function (event) {
    let feed_id = event.target.attributes.getNamedItem('data-feed_id').value;
    let reply_id = 'reply_' + feed_id;

    let reply_content = $('#' + reply_id).val();
    console.log(reply_content);

    if (reply_content.length <= 0) {
        alert('댓글 내용을 입력해주세요');
        return 0;
    }

    $.ajax({
        url: '/contents/reply/',
        data: {
            feed_id : feed_id,
            reply_content : reply_content
        },
        method: "POST",
        success: function (data) {
            console.log("성공");
            console.log(data);
            alert("댓글을 달았습니다.");
            // 해당 div 추가 시 html 화면에서 {{ user.nickname }}이 추가된 뒤에 새로고침을 해야 정상적인 nickname이 출력되는 오류가 있어
            // 서버 쪽에서 nickname 정보를 받아오도록 변경
            $('#reply_list_' + feed_id).append("<div class='feed_comment'><b>" + data.user_nickname + "</b>&nbsp;" + reply_content + "</div>")
        },
        error: function () {
            console.log("에러 발생");
        },
        complete: function () {
            console.log("완료")
            $('#' + reply_id).val('');
        }
    });
});
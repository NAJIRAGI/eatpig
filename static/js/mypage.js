/** HTML에서 Email 정보 받기 **/
const userEmailElement = document.getElementById('userEmail');
const userEmail = userEmailElement.getAttribute('data-email');

$('#btn_profile_upload').click(function (){
   $('#input_file_upload').click();
});

function profile_upload() {
    let file = $('#input_file_upload')[0].files[0];
    let email = userEmail

    let fd = new FormData();

    fd.append('file', file);
    fd.append('email', email)

    $.ajax({
        url: "/accounts/updateimg/",
        data: fd,
        method: "POST",
        processData: false,
        contentType: false,
        success: function (data) {
            console.log('성공');
        },
        error: function () {
            console.log('에러')
        },
        complete: function () {
            console.log('완료')
            location.replace('/accounts/mypage/')
        }
    });

}

$('#btn_my_feed').click(function () {
    $('#my_feed_list').css({
        "display": "flex",
    });
    $('#btn_my_feed').css({
        "font-weight": "bold"
    });
    $('#my_like_feed_list').css({
        "display": "none"
    });
    $('#btn_my_like').css({
        "font-weight": "normal"
    });
    $('#my_bookmark_feed_list').css({
        "display": "none"
    });
    $('#btn_my_bookmark').css({
        "font-weight": "normal"
    });
})

$('#btn_my_like').click(function () {
     $('#my_feed_list').css({
        "display": "none",
    });
    $('#btn_my_feed').css({
        "font-weight": "normal"
    });
    $('#my_like_feed_list').css({
        "display": "flex"
    });
    $('#btn_my_like').css({
        "font-weight": "bold"
    });
    $('#my_bookmark_feed_list').css({
        "display": "none"
    });
    $('#btn_my_bookmark').css({
        "font-weight": "normal"
    });
})

$('#btn_my_bookmark').click(function () {
    $('#my_feed_list').css({
        "display": "none",
    });
    $('#btn_my_feed').css({
        "font-weight": "normal"
    });
    $('#my_like_feed_list').css({
        "display": "none"
    });
    $('#btn_my_like').css({
        "font-weight": "normal"
    });
    $('#my_bookmark_feed_list').css({
        "display": "flex"
    });
    $('#btn_my_bookmark').css({
        "font-weight": "bold"
    });
})
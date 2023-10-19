$('#update_btn').click(function () {
    let oldPassword = $('#old_password').val();
    let newPassword = $('#new_password').val();
    let newNickname = $('#new_nickname').val();
    console.log(oldPassword)
    console.log(newPassword)
    console.log(newNickname)

    $.ajax({
        url: "/accounts/update/",
        data: {
            old_password: oldPassword,
            new_password: newPassword,
            new_nickname: newNickname
        },
        method: "POST",
        success: function (data) {
            alert(data.message);
            location.replace('/accounts/mypage/')
        },
        error: function (request, status, error) {
            if(request.responseJSON && request.responseJSON.message){
                alert(request.responseJSON.message);
             }else{
                 alert("알 수 없는 오류가 발생했습니다, 관리자에게 문의 부탁드립니다.");
             }
            console.log('에러가 발생 했습니다.');
        },
        complete: function () {
            console.log('완료');

        }
    });
});
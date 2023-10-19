$('#login_btn').click(function () {

    let email = $('#input_email').val();
    let password = $('#input_password').val();

     if(!email || !password){
        alert("비어있는 곳이 있습니다, 내용을 입력 해주세요.");
        return;
    }

    console.log(email, password);

    $.ajax({
        url: "/accounts/login/",
        data: {
            email: email,
            password: password
        },
        method: "POST",
        success: function (data) {
            console.log('성공');
            alert("로그인 성공");
            location.replace('/contents/content_list/');
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
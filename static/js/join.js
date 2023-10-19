$('#join_btn').click(function (){

    let email = $('#input_email').val();
    let password = $('#input_password').val();
    let nickname = $('#input_nickname').val();
    let name = $('#input_name').val();

    if(!email || !password || !nickname || !name){
        alert("비어있는 곳이 있습니다, 내용을 입력 해주세요.");
        return;
    }

    console.log(email, password, nickname, name);

    $.ajax({
        url: "/accounts/join/",
        data: {
            email : email,
            password : password,
            nickname : nickname,
            name : name
        },
        method: "POST",
        success: function (data) {
            console.log('업로드 성공');
            alert("회원가입을 완료했습니다, 로그인해주세요");
            location.replace('/accounts/login/');
        },
        error: function (request, status, error) {
            console.log('에러가 발생 했습니다.');
            if(request.responseJSON && request.responseJSON.message){
                alert(request.responseJSON.message);
             }else{
                 alert("알 수 없는 오류가 발생했습니다, 관리자에게 문의 부탁드립니다.");
             }
        },
        complete: function () {
            console.log('완료');
        }
    });
});
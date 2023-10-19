$('#delete-account-button').click(function() {
  let password = $('#delete-account-password').val();

  $.ajax({
      url: '/accounts/delete/',
      method: 'POST',
      data: {
          mypassword: password
      },
      success: function (data) {
            alert(data.message);
            location.replace('/accounts/login/')
      },
      error: function(request, status, error) {
          if(request.responseJSON && request.responseJSON.message){
              alert(request.responseJSON.message);
           }else{
               alert("알 수 없는 오류가 발생했습니다, 관리자에게 문의 부탁드립니다.");
           }
          console.log('에러가 발생 했습니다.');
      }
  });
});
from django.urls import path

from account.views import Join, Login, LogOut, Mypage, UpdateProfileImg, UpdateAccount, DeleteAccount

app_name = 'account'

urlpatterns = [
    path('join/', Join.as_view()),
    path('login/', Login.as_view()),
    path('logout/', LogOut.as_view()),
    path('mypage/', Mypage.as_view()),
    path('updateimg/', UpdateProfileImg.as_view()),
    path('update/', UpdateAccount.as_view()),
    path('delete/', DeleteAccount.as_view())
]

import os
from uuid import uuid4

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from content.models import Content, Like, Bookmark
from eatpig.settings.base import MEDIA_ROOT


# Create your views here.

class Join(APIView):
    def get(self, request):
        return render(request, 'account/join.html')

    def post(self, request):
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return Response(status=400, data=dict(message="유효하지 않은 이메일 형식입니다."))

        Account.objects.create(email=email,
                               nickname=nickname,
                               name=name,
                               password=make_password(password),
                               profile_img='default_profile.jpg')
        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = Account.objects.filter(email=email).first()  # list 형태로 넘어오는 Query Set의 첫번째 Data를 filtering

        if user is None:
            return Response(status=400, data=dict(message="회원 정보가 잘못 되어 있습니다."))

        if user.check_password(password):
            # 로그인을 했다는 정보, session or cookie
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원 정보가 잘못 되어 있습니다."))


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "account/login.html")


class Mypage(APIView):
    def get(self, request):

        user = Account.objects.filter(email=request.session.get('email')).first()

        if user is None:
            return render(request, "account/login.html")

        my_feed_list = Content.objects.filter(user=user)

        my_like_list = list(Like.objects.filter(user=user, is_like=True).values_list('feed_id', flat=True))
        my_like_feed_list = Content.objects.filter(id__in=my_like_list)

        my_bookmark_list = list(Bookmark.objects.filter(user=user, is_marked=True).values_list('feed_id', flat=True))
        my_bookmark_feed_list = Content.objects.filter(id__in=my_bookmark_list)

        return render(request, 'account/mypage.html', context=dict(user=user,
                                                                   my_feed_list=my_feed_list,
                                                                   my_like_feed_list=my_like_feed_list,
                                                                   my_bookmark_feed_list=my_bookmark_feed_list))


class UpdateProfileImg(APIView):
    def post(self, request):
        file = request.FILES['file']

        uuid_name = uuid4().hex

        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_img = uuid_name

        user = Account.objects.filter(email=request.data.get('email')).first()

        user.profile_img = profile_img
        user.save()

        return Response(status=200)


class UpdateAccount(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return Response(status=400, data=dict(message="로그인을 해주세요"))

        user = Account.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="다시 확인 해주세요"))

        context = {
            'email': user.email,
            'nickname': user.nickname,
            'name': user.name,
        }
        return render(request, 'account/update.html', context)

    def post(self, request):
        email = request.session.get('email', None)
        if email is None:
            return Response(status=400, data=dict(message="로그인을 해주세요"))

        user = Account.objects.filter(email=email).first()

        old_password = request.POST.get("old_password", None)
        new_nickname = request.POST.get("new_nickname", None)
        new_password = request.POST.get("new_password", None)
        if not check_password(old_password, user.password):
            return Response(status=400, data=dict(message="기존 비밀번호를 다시 확인해주세요"))

        if check_password(new_password, user.password):
            return Response(status=400, data=dict(message="새로운 비밀번호는 기존의 비밀번호와 달라야 합니다."))

        user.nickname = new_nickname
        user.set_password(new_password)
        user.save()
        return Response(status=200, data=dict(message="회원정보 변경완료"))


class DeleteAccount(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return Response(status=400, data=dict(message="로그인을 해주세요"))
        user = Account.objects.filter(email=email).first()
        if user is None:
            return Response(status=400, data=dict(message="다시 확인 해주세요"))

        context = {
            'email': user.email,
            'nickname': user.nickname,
            'name': user.name,
            'profileImg': user.profile_img
        }
        return render(request, 'account/delete.html', context)

    def post(self, request):
        email = request.session.get('email', None)
        if email is None:
            return Response(status=400, data=dict(message="로그인을 해주세요"))

        user = Account.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="다시 확인 해주세요"))

        mypassword = request.data.get('mypassword')

        if not check_password(mypassword, user.password):
            return Response(status=400, data=dict(message="비밀번호를 다시 확인해주세요"))
        user.delete()
        # 세션도 삭제하여 로그아웃 상태로 변경.
        request.session.flush()
        # 200 상태 코드와 함께 메시지 반환
        return Response(status=200, data=dict(message="회원 탈퇴가 완료되었습니다."))

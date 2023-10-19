import os.path
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from eatpig.settings import MEDIA_ROOT
from .models import Content, Reply, Like, Bookmark


# Create your views here.
class Contents(APIView):
    def get(self, request):
        user = Account.objects.filter(email=request.session.get('email')).first()

        selected_region = request.GET.get('region')
        selected_menu = request.GET.get('menu')
        feed_object_list = Content.objects.all()

        if selected_region:
            feed_object_list = feed_object_list.filter(region=selected_region)

        if selected_menu:
            feed_object_list = feed_object_list.filter(menu=selected_menu)

        feed_object_list = feed_object_list.order_by('-id')  # select * from content_Contents;
        feed_list = []

        for feed in feed_object_list:
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                reply_user = Account.objects.filter(id=reply.user_id).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=reply_user.nickname))
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, user=user, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, user=user, is_marked=True).exists()

            feed_user = Account.objects.get(id=feed.user_id)

            like = Like.objects.filter(feed_id=feed.id, is_like=True).order_by('-id').first()

            if like:
                like_user = Account.objects.get(id=like.user_id)
                last_liked_user = dict(nickname=like_user.nickname,
                                       user_profile=like_user.profile_img)
            else:
                last_liked_user = None

            feed_list.append(dict(id=feed.id,
                                  diner=feed.diner,
                                  image=feed.image,
                                  content=feed.contents,
                                  like_count=like_count,
                                  profile_img=feed_user.profile_img,
                                  nickname=feed_user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked,
                                  region=feed.region,
                                  menu=feed.menu,
                                  last_liked_user=last_liked_user))

        if user is None:
            return render(request, "account/login.html")

        return render(request, "content/content_list.html", context=dict(feed_list=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        # 파일 불러 오기
        file = request.FILES['file']
        # 이름을 영어와 숫자로 이루어진 랜덤으로 지정 하기
        uuid_name = uuid4().hex
        # 저장 시 미디어 경로 뒤에 랜덤으로 정해진 이름을 합쳐서 저장
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        # 파일 저장
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        contents = request.data.get('content')
        email = request.session.get('email', None)
        region = request.data.get('region')
        menu = request.data.get('menu')
        diner = request.data.get('diner')
        user = Account.objects.get(email=email)

        Content.objects.create(image=image, contents=contents, user=user, region=region, menu=menu, diner=diner)

        return Response(status=200)


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)
        user = Account.objects.get(email=email)
        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, user=user)
        # 서버에서 받아서 쓸 때 변수 명 user_nickname에 user의 nickname 정보를 저장해서 전달
        return Response({'user_nickname': user.nickname}, status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)
        print(favorite_text)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False

        email = request.session.get('email', None)
        user = Account.objects.get(email=email)

        like = Like.objects.filter(feed_id=feed_id, user=user).first()
        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, user=user)

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        print(bookmark_text)

        print(bookmark_text)
        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False

        email = request.session.get('email', None)
        user = Account.objects.get(email=email)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, user=user).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, user=user)

        return Response(status=200)


class DeleteFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        email = request.session.get('email', None)
        user = Account.objects.get(email=email)

        feed = Content.objects.get(id=feed_id, user=user)
        feed.delete()

        return Response(status=200)


class MenuPage(APIView):
    def get(self, request):
        return render(request, 'content/menupage.html')


class RegionPage(APIView):
    def get(self, request):
        return render(request, 'content/regionpage.html')

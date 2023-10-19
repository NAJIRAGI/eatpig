from django.urls import path

from content.views import Contents, UploadFeed, UploadReply, ToggleLike, ToggleBookmark, DeleteFeed, MenuPage, \
    RegionPage

from . import views

app_name = 'content'

urlpatterns = [
    path('content_list/', Contents.as_view()),
    path('upload', UploadFeed.as_view()),
    path('reply/', UploadReply.as_view()),
    path('like/', ToggleLike.as_view()),
    path('bookmark/', ToggleBookmark.as_view()),
    path('content_delete', DeleteFeed.as_view()),
    path('menupage/', MenuPage.as_view()),
    path('regionpage/', RegionPage.as_view())
]

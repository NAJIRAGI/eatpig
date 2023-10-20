from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from content.views import Contents, UploadFeed
from eatpig.settings import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('content.urls')),
    path('contents/', include('content.urls')),
    path('accounts/', include('account.urls'))
]

urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

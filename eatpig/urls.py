from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from content.views import Contents, UploadFeed
from eatpig import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contents/', include('content.urls')),
    path('accounts/', include('account.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

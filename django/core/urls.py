from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # General app URLs
    path('', include('general.urls')),
    path('download/', include('downloaddata.urls')),
    # CKEditor file uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Django admin
    path('dashboard/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

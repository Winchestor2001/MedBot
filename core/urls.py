from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from .yasg import urlpatterns as yasg_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("med_app.urls")),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += yasg_urlpatterns

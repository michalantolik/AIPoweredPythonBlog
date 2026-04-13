from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cms/", include("wagtail.admin.urls")),
    path("documents/", include("wagtail.documents.urls")),
    path("_plantuml/", include("cms.urls")),
    path("api/", include("api.urls")),
    path("", include("website.urls")),
    path("health/", health),
    path("", include("wagtail.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger_doc"),
]

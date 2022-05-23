from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import PDFView, UserLogin

router = DefaultRouter()

router.register(r"pdf", PDFView, basename="base_pdf")

app_name = "api"
urlpatterns = [
    path("", include(router.urls), name="pdf"),
    path("superuser/login/", UserLogin.as_view(), name="login"),
]

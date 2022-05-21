from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import PDFView, UserLogin

router = DefaultRouter()

router.register(r"pdf", PDFView, basename="pdf")

urlpatterns = [
    path("", include(router.urls)),
    path("superuser/login/", UserLogin.as_view(), name="login"),
]

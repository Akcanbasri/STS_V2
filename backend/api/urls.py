from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    StudentCreateViewSet,
    TeacherCreateViewSet,
    ParentCreateViewSet,
    AdminCreateViewSet,
)

router = DefaultRouter()
router.register(r"students", StudentCreateViewSet, basename="students")
router.register(r"teachers", TeacherCreateViewSet, basename="teachers")
router.register(r"parents", ParentCreateViewSet, basename="parents")
router.register(r"admins", AdminCreateViewSet, basename="admins")

urlpatterns = [
    path("", include(router.urls)),
    # JWT Token URLs
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

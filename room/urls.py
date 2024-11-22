from django.urls import path  # type: ignore
from rest_framework.routers import SimpleRouter  # type: ignore
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from room import views

app_name = "room"

user_api_router = SimpleRouter()
user_api_router.register("user/api", views.user_API_ViewSet, basename="user-api")

room_api_router = SimpleRouter()
room_api_router.register("room/api", views.room_API_ViewSet, basename="room-api")

component_api_router = SimpleRouter()
component_api_router.register(
    "component/api", views.component_API_ViewSet, basename="component-api"
)

urlpatterns = [
    path("user/register/", views.UserView.as_view(), name="user-register"),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("room/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("room/api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("room/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += user_api_router.get_urls()
urlpatterns += room_api_router.get_urls()
urlpatterns += component_api_router.get_urls()
# print(urlpatterns)

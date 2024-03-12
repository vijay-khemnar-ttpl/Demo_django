from django.urls import path

from .views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    LoginLogoutView,
    UserAPIView
)



app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),

    path("api/v1/login", LoginLogoutView.as_view({"post":"user_login"}), name="login"),
    path("api/v1/logout", LoginLogoutView.as_view({"post":"user_logout"}), name="logout"),
    path("api/v1/refresh", LoginLogoutView.as_view({"post":"refresh_token"}), name="refresh_token"),

    path("api/v1/registration", UserAPIView.as_view({"post":"create"}), name="user_registration"),

]

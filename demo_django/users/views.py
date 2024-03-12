from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from demo_django.users.models import User, CustomUserManager

from django.contrib.auth import authenticate, logout
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView

# from demo_django.common.password_token_generator import make_random_password
# from demo_django.common.send_email import send_registration_mail

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class LoginLogoutView(viewsets.ViewSet, TokenRefreshView):
    permission_classes = [AllowAny]

    def user_login(self, request):
        '''
            User Login API
            Required fields:
            1) Email
            2) Password
        '''
        request_data = dict(request.data)
        email = request_data.get("email", "")
        password = request_data.get("password", "")
        if not email or not password:
            return Response({"error": "Invalid Credentials!"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid Credentials!"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        login_data = {
            "token": {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            "message": "Logged in successfully."
        }
        return Response(login_data, status=status.HTTP_200_OK)

    def user_logout(self, request):
        '''
            User logout API
        '''
        logout(request)
        return Response({"message": "User logged out successfullly!"}, status=status.HTTP_200_OK)

    def refresh_token(self, request, *args, **kwargs):
        try:
            '''
                User token refresh API
                refresh token is required
            '''
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                login_data = {
                        "token": {
                            "refresh": request.data["refresh"],
                            "access": response.data['access'],
                        },
                        "message": "Logged in successfully."
                    }
                return Response(login_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)


class UserAPIView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        request_data = dict(request.data)
        custom_user_manager = CustomUserManager()
        if not request_data.get("email", ""):
            return Response({"error": "Email is required for registration."}, status=status.HTTP_400_BAD_REQUEST)
        password = request_data.get("password", "")
        if not password:
            return Response({"error": "Password is required for registration."}, status=status.HTTP_400_BAD_REQUEST)
        # password = make_random_password(length=12)
        extra_fields = {
            "name": request_data.get("name", "").title(),
        }
        try:
            user_object = custom_user_manager.create_normal_user(
                email=request_data.get("email").lower(),
                password=password,
                **extra_fields
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if user_object:
            return Response({"message": "User registered successfullly!"}, status=status.HTTP_201_CREATED)
        return Response({"error": "User registration failed"}, status=status.HTTP_400_BAD_REQUEST)

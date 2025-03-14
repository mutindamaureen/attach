from django.urls import path
from .views import RegisterView, get_user_profile, login_view, EditProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", login_view, name="login"),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', get_user_profile, name='user-profile'),
    path("profile/edit/", EditProfileView.as_view(), name="edit-profile"),

]

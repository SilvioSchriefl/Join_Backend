
from django.contrib import admin
from django.urls import path
from task.views import LoginView, RegisterView, LogoutView, UserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', LoginView.as_view(), name='get_token'),
    path('sign_up/', RegisterView.as_view(), name='register'),
    path('log_out/', LogoutView.as_view(), name='logout'),
    path('users/', UserView.as_view(), name='logout'),
]

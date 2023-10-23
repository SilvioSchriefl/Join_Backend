
from django.contrib import admin
from django.urls import path
from task.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', LoginView.as_view(), name='get_token'),
]


from django.contrib import admin
from django.urls import path
from task.views import LoginView, RegisterView, LogoutView, UserView, ContactView, ContactListView, CategoryView, TaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', LoginView.as_view(), name='get_token'),
    path('sign_up/', RegisterView.as_view(), name='register'),
    path('log_out/', LogoutView.as_view(), name='logout'),
    path('users/', UserView.as_view(), name='logout'),
    path('add_contact/', ContactView.as_view(), name='add_contact'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('edit_contact/<int:user_id>/', ContactListView.as_view(), name='edit_contacts'),
    path('contact/<int:user_id>/', ContactListView.as_view(), name='delete_contact'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<int:id>/', CategoryView.as_view(), name='delete_category'),
    path('task/', TaskView.as_view(), name='task'),
 
 
]

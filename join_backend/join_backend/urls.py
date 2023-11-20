
from django.contrib import admin
from django.urls import path
from task.views import LoginView, RegisterView, LogoutView, UserView, ContactView, CategoryView, TaskView, DeleteContactView, EditContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', LoginView.as_view(), name='get_token'),
    path('sign_up/', RegisterView.as_view(), name='register'),
    path('log_out/', LogoutView.as_view(), name='logout'),
    path('users/', UserView.as_view(), name='users'),
    path('contacts/', ContactView.as_view(), name='add_contact'),
    path('edit_contact/<int:contact_id>/', EditContactView.as_view(), name='edit_contacts'),
    path('delete_contact/<int:contact_id>/', DeleteContactView.as_view(), name='delete_contact'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<int:id>/', CategoryView.as_view(), name='delete_category'),
    path('task/', TaskView.as_view(), name='task'),
    path('task/<int:id>/', TaskView.as_view(), name='delete_task'),
 
 
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'), #Check a user's profile
    path('search/', views.user_search, name='user_search'), #Search through all users
    path('delete_update/<int:update_id>/', views.delete_update, name='delete_update'), #Delete update 
     path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'), #Hide notification
]
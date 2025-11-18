from django.urls import path
from .views import RegisterView, LoginView, NotificationListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('notifications/', NotificationListView.as_view(), name='user-notifications'),
]

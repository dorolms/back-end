from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/communications/', include('communications.urls')),
    path('api/lectures/', include('lectures.urls')),
]
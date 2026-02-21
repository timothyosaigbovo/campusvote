"""
URL configuration for the CampusVote project.

Routes requests to the appropriate app based on URL prefix:
- /accounts/ → User authentication and profiles
- /elections/ → Student-facing election features
- /management/ → Admin CRUD and analytics
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('elections/', include('elections.urls')),
    path('management/', include('management.urls')),
    path('', include('elections.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# Custom error handlers
handler404 = 'elections.views.custom_404'
handler500 = 'elections.views.custom_500'
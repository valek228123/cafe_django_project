"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from table import views as tabel_views
from reservation import views as reservation_views
from authentication import views as auth_views
from reservation.api.urls import router as reservation_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tabel_views.IndexView.as_view(),name = 'index'),
    path('tables/',include('table.urls')),
    path('reservation/',include('reservation.urls')),
    path("auth/",include('authentication.urls')),
    path("api/reservations/",include(reservation_router.urls)),
    path("api/users/",include('authentication.api.urls')),
    path("api/auth/", include('djoser.urls.authtoken')),
    path("api/auth", include('djoser.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
] + debug_toolbar_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




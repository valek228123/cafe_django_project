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
# from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from table import views as tabel_views
from reservation import views as reservation_views
from authentication import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tabel_views.index_view,name = 'index'),
    path('tables/', tabel_views.table_view, name = 'tabels-list'),
    path('tables/book_a_table/<int:table_id>',reservation_views.book_table_view, name = 'book-table'),
    path('tables/list_booked_tables', reservation_views.list_booked_tables_view, name = 'list-booked-tables'),
    path('tables/list_booked_tables/delete/<int:reservation_id>',reservation_views.delete_booked_table_view, name = 'delete-booked-table'),
    path('auth/register', auth_views.register_view, name='register'),
    path('auth/login', auth_views.LoginView.as_view(), name = 'login'),
    path('auth/logout/', LogoutView.as_view(), name = 'logout'),
]
# + debug_toolbar_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




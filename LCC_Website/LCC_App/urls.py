from django.urls import path
from LCC_App import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView


app_name = 'LCC_App'

urlpatterns = [
    path('', views.home, name='home'),
    path('library/', views.search_books, name='list_books'),
    path('concurrent/', views.add_concurrent, name='add_concurrent'),
    path('events/', views.list_events, name='list_events'),
    path('login/', views.connect, name='custom_login'),
    path('admin/login/',LoginView.as_view(), name='admin_login'),
    path('logout/', views.logout, name='logout'),
    path('library/view_pdf/<str:pk>/', views.view_pdf, name='view_pdf'),
    path('add_to_library/<str:book_pk>/', views.add_to_library, name='add_to_library'),
    # ... other URL patterns ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
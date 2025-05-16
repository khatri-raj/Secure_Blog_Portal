from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('add/',views.add, name='add'),
    path('show/', views.show, name='show'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('help/', views.help, name='help'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('magic-link/', views.magic_link_view, name='magic_link'),
    path('magic-link-sent/', views.magic_link_sent_view, name='magic_link_sent'),
    path('verify-magic-link/<uuid:token>/', views.verify_magic_link_view, name='verify_magic_link'),
]
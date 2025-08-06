from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entry/<int:entry_id>/', views.view_entry, name='entry_detail'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='entry_delete'),
    path('download/<int:entry_id>/', views.download_pdf, name='download_pdf'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('generate/', views.generate_content, name='generate_content'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

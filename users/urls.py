from django.urls import path

from . import views

app_name = "users"

urlpatterns = [    
    path('register/', views.register_view, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    
]
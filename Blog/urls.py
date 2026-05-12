from venv import create

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    # Register (your custom view)
    path('register/', views.register, name='register'),

    # Login / Logout (built-in)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('create/', views.create_post, name='create_post'),
    path('update/<int:id>/', views.update_post, name='update_post'),
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
    path('post/<int:id>/', views.post_detail , name='post_detail'),
    path('like/<int:id>/', views.like_post, name='like_post'),
    path('profile/<str:username>/',views.profile, name='profile'),
    path('edit-profile/', views.edit_profile , name='edit_profile'),
path('add-comment/<int:id>/', views.add_comment, name='add_comment'),
path( 'save/<int:id>/', views.save_post,name='save_post'),
path('saved-posts/',views.saved_posts,name='saved_posts'),
]
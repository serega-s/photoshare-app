from django.urls import path

from . import views

urlpatterns = [
    path('', views.gallery, name="gallery"),
    path('photo/by_<str:username>/', views.photos_by_user, name="photos_by_user"),
    path('add/', views.add_photo, name="add"),
    path('photo/<str:pk>/', views.view_photo, name="photo"),
    path('add_comment/', views.add_comment),

    path('user/<str:username>/', views.profile, name='profile'),
    path('user/<str:username>/followers/', views.followers, name='followers'),
    path('user/<str:username>/follows/', views.follows, name='follows'),
    path('user/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('user/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
]

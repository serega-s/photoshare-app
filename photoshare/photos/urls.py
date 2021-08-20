from django.urls import path

from . import views

urlpatterns = [
    path('', views.Gallery.as_view(), name="gallery"),
    path('photo/user/by_<str:username>/',
         views.UserGallery.as_view(), name="photos_by_user"),
    path('photo/add/', views.AddPhoto.as_view(), name="add"),
    path('photo/<str:pk>/', views.ViewPhoto.as_view(), name="photo"),
    path('add_comment/', views.AddComment.as_view()),

    path('user/<str:username>/', views.UserProfile.as_view(), name='profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('user/<str:username>/followers/',
         views.Followers.as_view(), name='followers'),
    path('user/<str:username>/follows/',
         views.Follows.as_view(), name='follows'),
    path('user/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('user/<str:username>/unfollow/',
         views.unfollow_user, name='unfollow_user'),
]

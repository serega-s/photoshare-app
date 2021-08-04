from django.urls import path

from . import views

urlpatterns = [
    path('', views.gallery, name="gallery"),
    path('photo/by_<str:name>/', views.photos_by_user, name="photos_by_user"),
    path('add/', views.add_photo, name="add"),
    path('photo/<str:pk>/', views.view_photo, name="photo"),
    path('add_comment/', views.add_comment)
]

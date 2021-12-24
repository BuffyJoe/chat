from django.urls import path
from application import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('home/', views.index, name="home"),
    path('group/<int:pk>/', views.groupview, name="group"),
    path('group/', views.joingroup, name="Join"),
    path('edit/<int:pk>/', views.edit, name="edit"),
    path('create/', views.create, name="create"),
    path('delete/<int:pk>/', views.deleteGroup, name="delete"),
    path('log-out/', views.logoutpage, name='log-out'),
    path('log-in/', views.Loginpage, name='log-in'),
    path('sign-up/', views.register, name='sign-up')
]
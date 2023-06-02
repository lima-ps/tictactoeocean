from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register/", views.register, name='register'),
    path("login/", views.loginPage, name='login'),
    path("logout/", views.logoutPage, name='logout'),
    path("game/<int:roomNumber>/<int:playerId>/", views.game),
]
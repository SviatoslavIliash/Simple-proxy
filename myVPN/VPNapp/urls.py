from django.urls import path
from VPNapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("userPage/", views.user_page, name="user_page"),
    path("login/", views.user_login, name="user_login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path("<str:alias>/<path:site_path>/", views.my_alias_view, name="my_alias_view"),
    path("<str:alias>/", views.my_alias_view, name="my_alias_view"),

]

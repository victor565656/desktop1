from django.urls import path

from . import views

app_name="auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("pag1", views.pag1, name="pag1"),
    path("negado", views.negado, name="negado"),
    path("parcial", views.parcial, name="parcial"),
    path("ver", views.ver, name="ver"),
    path('ver_grupo/<str:grupo_id>', views.ver_grupo, name="ver_grupo"),
    path('archivos/<str:grupo_id>', views.archivos, name="archivos"),
    path('archivos/<str:grupo_id>', views.archivos, name="archivos"),
    path("download/<str:id>", views.download, name="download"),
]

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

    #ver grupos y usuarios y crear grupo
    path("ver", views.ver, name="ver"),
    path("crear_grupo", views.crear_grupo, name="crear_grupo"),

    #ver grupo especifico y agregar miembros
    path('ver_grupo/<str:grupo_id>', views.ver_grupo, name="ver_grupo"),
    path('agregar_miembro/<str:grupo_id>', views.agregar_miembro, name="agregar_miembro"),

    #subir y bajar archivos en grupo especifico
    path('archivos/<str:grupo_id>', views.archivos, name="archivos"),
    path("download/<str:id>", views.download, name="download"),
    path("borrar_archivo/<str:grupo_id>/<str:archivo_id>", views.borrar_archivo, name="borrar_archivo"),
]

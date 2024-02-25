from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Grupo, Archivos
from django import forms
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.http import FileResponse




def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        # Se especifico el backend, debido a django-guardian ahora hay 2 en settings
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


#probando el decorador login_required
@login_required(login_url="auctions:negado")
def pag1(request):
    return render(request, "auctions/pag1.html")

def negado(request):
    return render(request, "auctions/negado.html")

def parcial(request):
    if not request.user.is_authenticated:
        mensaje = "no estas autentificado, ELEMENTO NEGADO"
    else:
        mensaje = "Autentificado, VIENDO ELEMENTO"
    
    return render(request, "auctions/parcial.html",{
        "mensaje": mensaje
    })






class Gruposform(forms.Form):
    nombre = forms.CharField(max_length=64)

def ver(request):
    grupos_disponibles = get_objects_for_user(request.user, 'auctions.view_grupo')
    return render(request, "auctions/ver.html",{
        "usuarios": User.objects.all(),
        "grupos": grupos_disponibles,
        "form": Gruposform(),
        "actual":request.user
    })


def crear_grupo(request):
    if request.method == "POST":
        form = Gruposform(request.POST)
        if form.is_valid():
            # Finding the passenger id from the submitted form data
            nombre = form.cleaned_data["nombre"]
            usuario_actual=request.user
            instancia_grupo= Grupo.objects.create(nombre=nombre, creador =usuario_actual)

            grupo_permisos_creador = Group.objects.create(name=f"creador_{instancia_grupo.id}")
            assign_perm('view_grupo', grupo_permisos_creador, instancia_grupo)
            assign_perm('add_grupo', grupo_permisos_creador, instancia_grupo)
            assign_perm('change_grupo', grupo_permisos_creador, instancia_grupo)
            assign_perm('delete_grupo', grupo_permisos_creador, instancia_grupo)
            usuario_actual.groups.add(grupo_permisos_creador)

            grupo_permisos_miembro = Group.objects.create(name=f"miembros_{instancia_grupo.id}")
            assign_perm('view_grupo', grupo_permisos_miembro, instancia_grupo)

        # Redirect user to flight page
        return HttpResponseRedirect(reverse("auctions:ver"))



def ver_usuario(request,usuario_id):
    usuario= User.objects.get(pk=usuario_id)
    return render(request, "auctions/ver_usuario.html",{
        "usuario": usuario,
        "archivos":usuario.archivos_de_usuario.all()
    })




class Mienbrosform(forms.Form):
    usuario = forms.IntegerField(min_value=1)

class Archivosform(forms.Form):
    nombre = forms.CharField(max_length=64)
    archivo = forms.FileField()


def ver_grupo(request, grupo_id):
    grupo = Grupo.objects.get(pk=grupo_id)
    
    if request.user.has_perm('auctions.view_grupo', grupo):
        return render(request, "auctions/ver_grupo.html",{
            "form": Mienbrosform(),
            "form2": Archivosform(),
            "grupo":grupo,
            "miembros": grupo.miembro.all(),
            "archivos": Archivos.objects.filter(grupo=grupo),
        })


def agregar_miembro(request,grupo_id):
    grupo = Grupo.objects.get(pk=grupo_id)
 
    if request.user.has_perm('auctions.change_grupo', grupo) and request.method == "POST":
        form = Mienbrosform(request.POST)

        if form.is_valid():
            # Finding the passenger id from the submitted form data
            usuario_id = form.cleaned_data["usuario"]
            usuario= User.objects.get(pk=usuario_id)
            grupo.miembro.add(usuario)

            miembros_grupo=Group.objects.get(name=f"miembros_{grupo.id}")
            usuario.groups.add(miembros_grupo)

        # Redirect user to flight page
        return HttpResponseRedirect(reverse("auctions:ver_grupo", args=(grupo_id,)))






def archivos(request, grupo_id):
    if request.method == "POST":
        form2 = Archivosform(request.POST, request.FILES)

        if form2.is_valid():
            nombre = form2.cleaned_data["nombre"]
            archivo = form2.cleaned_data["archivo"]
            grupo= Grupo.objects.get(pk=grupo_id)
            Archivos(publicador=request.user, grupo=grupo, nombre=nombre, archivo=archivo).save()
            
            return HttpResponseRedirect(reverse("auctions:ver_grupo", args=(grupo_id,)))
 

# para descargar archivos, recuerda dejar el link en el template con el url, NO agregar "download" en el link
def download(request, id):
    obj = Archivos.objects.get(id=id)
    filename = obj.archivo.path
    response = FileResponse(open(filename, 'rb'), as_attachment=True)
    return response

def borrar_archivo(request, archivo_id):
    obj = Archivos.objects.get(id=archivo_id)
    obj.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



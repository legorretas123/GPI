from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render_to_response, render, HttpResponseRedirect
from users.models import *
from django.contrib.auth.models import User
import datetime
import psycopg2
from mysite.vistas.forms import *
import os,binascii
import string
import random
from django.core.mail import send_mail
from django.contrib import auth
from pathlib import Path
import xlrd

###############################################################################
###############################################################################
def requiere_staff(view):
    def vista_nueva(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return view(request, *args, **kwargs)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    return vista_nueva
###############################################################################
###############################################################################


def Solicitudes(request):
    if (request.method=='GET'):
        solicitudes      =   Solicitud.objects()
        return render(request, 'home.html',locals())
    if (request.method=='POST'):
        return render(request, 'home.html')
    else:
        raise Http404()

def Nuevas(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/Login/')
    return render(request, 'home.html')


def CrearUsuario(request):
    if request.method == 'GET':
        form = FormCrearUsuario()
        return render(request, 'Super/CrearUsuario.html', locals())
    if request.method == 'POST':
        form = FormCrearUsuario(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            TOKEN = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
            p1 = User.objects.create_user(
                username=data['first_name']+data['last_name'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'])
            p1.save()
            p2= Profile(user = p1,tipo=data['tipo'],telefono=data['telefono'],token = TOKEN)
            p2.save()
            send_mail(
                'Activación de cuenta: GPI',
                'Bienvenido al sistema de activación de cuentas GPI.\n'+
                'Su nombre de usuario es: '+ data['first_name']+data['last_name']+'\n'+
                'ingrese al link para elegir su password: http://127.0.0.1:8000/Activate/'+TOKEN,
                'gpi.ingsoftware@gmail.com',
                ['gpi.ingsoftware@gmail.com'],#cambiar por data['email']
                fail_silently=False,
            )
            return HttpResponseRedirect('/')
        return render(request, 'Super/CrearUsuario.html', locals())
    else:
        raise Http404()


def VerUsuarios(request):
    if request.method == 'GET':
        perfiles      =   Profile.objects.order_by("id")
        return render(request, 'Super/VerUsuarios.html', locals())
    else:
        raise Http404()

def VerMateriales(request):
    if request.method == 'GET':
        materiales      =   MaterialReal.objects.all()
        return render(request, 'Super/VerMateriales.html', locals())
    else:
        raise Http404()

def VerProveedores(request):
    if request.method == 'GET':
        proveedores      =  Proveedor.objects.all()
        return render(request, 'Super/VerProveedores.html', locals())
    else:
        raise Http404()

def VerBodegas(request):
    if request.method == 'GET':
        bodegas      =   Bodega.objects.all()
        return render(request, 'Super/VerBodegas.html', locals())
    else:
        raise Http404()

def EliminarUsuario(request,offset):
    if request.method == 'GET':
        usuario = User.objects.get(username=offset)
        usuario.delete()
        return HttpResponseRedirect('/Usuarios/Ver/')
    else:
        raise Http404()
def EliminarBodega(request,offset):
    if request.method == 'GET':
        bodega = Bodega.objects.get(nombre=offset)
        bodega.delete()
        return HttpResponseRedirect('/Bodegas/Ver/')
    else:
        raise Http404()


def CargarMateriales(request):
    if request.method == 'GET':
        form = FormCargarMateriales()
        return render(request, 'Super/CargarMateriales.html', locals())
    if request.method == 'POST':
        form = FormCargarMateriales(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            input_excel = request.FILES['data']
            book = xlrd.open_workbook(file_contents=input_excel.read())
            first_sheet = book.sheet_by_index(0)
            bodega_i=Bodega.objects.get(nombre=data['bodega'])
            for i in range(first_sheet.nrows):
                categoria_i         =first_sheet.cell(i,0).value.lower()
                codigo_i            =first_sheet.cell(i,1).value.lower()
                nombre_i            =first_sheet.cell(i,2).value.lower()
                marca_i             =first_sheet.cell(i,3).value.lower()
                caracteristicas_i   =first_sheet.cell(i,4).value.lower()
                cantidad_i          =int(first_sheet.cell(i,5).value)
                if not MaterialAbstracto.objects.filter(nombre=nombre_i).exists():
                    MaterialAbstracto_i = MaterialAbstracto(nombre=nombre_i,categoria=categoria_i)
                    MaterialAbstracto_i.save()
                if not MaterialCategoria.objects.filter(categoria=categoria_i).exists():
                    MaterialCategoria_i = MaterialCategoria(categoria=categoria_i)
                    MaterialCategoria_i.save()
                # if not MaterialReal.objects.filter(codigo=codigo_i).exists():
                MaterialAbstracto_i=MaterialAbstracto.objects.get(nombre=nombre_i)
                MaterialReal_i = MaterialReal(
                                        categoria=categoria_i,
                                        material=MaterialAbstracto_i,
                                        codigo=codigo_i,
                                        marca=marca_i,
                                        caracteristicas=caracteristicas_i,
                                        cantidad=cantidad_i,
                                        bodega = bodega_i
                                        )
                MaterialReal_i.save()
            return HttpResponseRedirect('/')
        return render(request, 'Super/CargarMateriales.html', locals())
    else:
        raise Http404()


def CargarProveedores(request):
    if request.method == 'GET':
        form = FormCargarProveedores()
        return render(request, 'Super/CargarProveedores.html', locals())
    if request.method == 'POST':
        form = FormCargarProveedores(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['data']
            book = xlrd.open_workbook(file_contents=input_excel.read())
            first_sheet = book.sheet_by_index(0)

            for i in range(first_sheet.nrows):
                categoria_i     =first_sheet.cell(i,0).value.lower()
                material_i      =first_sheet.cell(i,1).value.lower()
                empresa_i       =first_sheet.cell(i,2).value.lower()
                nombre_i        =first_sheet.cell(i,3).value.lower()
                email_i         =first_sheet.cell(i,4).value.lower()
                telefono_i      =str(first_sheet.cell(i,5).value)

                # if not Proveedor.objects.filter(nombre=nombre_i,material=material_i).exists():
                Proveedor_i=Proveedor(
                                    categoria = categoria_i,
                                    material=material_i,
                                    empresa=empresa_i,
                                    nombre=nombre_i,
                                    email=email_i,
                                    telefono=telefono_i
                                    )
                Proveedor_i.save()


            return HttpResponseRedirect('/')
        return render(request, 'Super/CargarProveedores.html', locals())
    else:
        raise Http404()







def CrearBodega(request):
    if request.method == 'GET':
        form = FormCrearBodega()
        return render(request, 'Super/CrearBodega.html', locals())
    if request.method == 'POST':
        form = FormCrearBodega(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bodega= Bodega(nombre = data['nombre'],ubicacion=data['ubicacion'])
            bodega.save()
            return HttpResponseRedirect('/')
        return render(request, 'Super/CrearBodega.html', locals())
    else:
        raise Http404()

def Business(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/Login/')
    return render(request, 'Business.html')

from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.contrib.auth.models import User
import datetime #necesario
import psycopg2 #necesario
from mysite.vistas.forms import *
import os,binascii
import string
import random
from django.core.mail import send_mail
from django.contrib import auth
from pathlib import Path
import xlrd
from users.models import *

###############################################################################
from django.db.models import Q
###############################################################################
def requiere_encargado(view):
    def vista_nueva(request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = Profile.objects.get(user=request.user)
            if perfil.tipo=='E':
                return view(request, *args, **kwargs)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    return vista_nueva

def VerBuzon(request):
    if request.method=='GET':
        items   =  Itemsol.objects.filter(estado="encargado")
        return render(request, 'Encargado/EncargadoBuzon.html',locals())
    else:
        raise Http404()

def ItemCotizar(request,ItemSolPk):
    if request.method=='GET':
        item   =  Itemsol.objects.get(pk=int(ItemSolPk))
        proveedores = Proveedor.objects.filter(Q(material=item.material.nombre) | Q(categoria=item.material.categoria))
        cotizaciones   =  Cotizacion.objects.filter(item=item).filter(respondido="yes")
        return render(request, 'Encargado/Cotizar.html',locals())
    else:
        raise Http404()

def Mail(request,ItemSolPK):
    item  =  Itemsol.objects.get(pk=ItemSolPK)
    proveedores = Proveedor.objects.filter(Q(material=item.material.nombre) | Q(categoria=item.material.categoria))
    for nombre in proveedores:
        TOKEN = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        cotizacion= Cotizacion(item=item,token = TOKEN,proveedor=nombre)
        cotizacion.save()
        send_mail(
            'GPI: Cotización, '+str(nombre.nombre),
            'Hola buenas tardes. Cotizamos con usted lo siguiente:.\n'+
                    str(item.material.categoria)+'\n'+
                    str(item.material.nombre)+'\n'+
                    str(item.descripcion)+'\n'+
                    str(item.cantidad_pedida)+str(item.unidad)+'\n'+
            'ingrese al link http://127.0.0.1:8000/Cotizar/Compra/'+TOKEN,
            'gpi.ingsoftware@gmail.com',
            ['gpi.ingsoftware@gmail.com'],#cambiar por data['email']
            fail_silently=False,
        )
    message="email de cotización enviado a los proveedores."
    return render(request, 'Encargado/Cotizar.html',locals())


def RespuestaProveedor(request,token):
    if request.method=='GET':
        try:
            cotizacion   =  Cotizacion.objects.get(token=token)
            form = FormularioCotizacion()
            return render(request, 'cotizacionForm.html', locals())
        except Cotizacion.DoesNotExist:
            html = "error."
            return HttpResponse(html)
        else:
            html = "error de sistema. envíe un email a gpi con su cotización."
            return HttpResponse(html)
    if request.method == 'POST':
        form = FormularioCotizacion(request.POST)
        if form.is_valid():
            print("YEAAAH")
            data = form.cleaned_data
            cotizacion   =  Cotizacion.objects.get(token=token)
            cotizacion.precio=data['precio']
            print(data['precio'])
            cotizacion.fecha=data['fecha']
            print(data['fecha'])
            cotizacion.comentarios=data['comentarios']
            print(data['comentarios'])
            cotizacion.respondido="yes"
            cotizacion.save()
            return HttpResponseRedirect('/')
        raise Http404()
    else:
        raise Http404()

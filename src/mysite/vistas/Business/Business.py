from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.contrib.auth.models import User
import datetime #necesario
import psycopg2
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
###############################################################################
def requiere_Business(view):
    def vista_nueva(request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = Profile.objects.get(user=request.user)
            if perfil.tipo=='C':
                return view(request, *args, **kwargs)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    return vista_nueva
###############################################################################
###############################################################################
def CrearObra(request):
    if request.method =='GET':
        form = FormCrearObra()
        return render(request, 'Business/CrearObra.html', locals())
    if request.method == 'POST':
        form = FormCrearObra(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            obra = Obra(nombre=data['nombre'],nombre_responsable=data['nombre_responsable'],ubicacion=data['ubicacion'],email=data['email'])
            obra.save()
            return HttpResponseRedirect('/')
        return render(request, 'Business/CrearObra.html', locals())
    else:
        raise Http404()

def CrearSolicitud(request):
    if request.method =='GET':
        form = FormCrearSolicitud()
        return render(request, 'Business/CrearSolicitud.html', locals())
    if request.method == 'POST':
            # class Solicitud(models.Model):
                fecha       = datetime.datetime.now()
                estado      = "abierto"
                bodeguero   = Profile.objects.get(pk=int(request.POST.getlist('bodeguero')[0]))
                ecompra     = None
                obra        = Obra.objects.get(nombre=request.POST.getlist('obra')[0])
                solicitud   =Solicitud(fecha=fecha,estado=estado,bodeguero=bodeguero,ecompra=ecompra,obra=obra)
                solicitud.save()
            # class Itemsol(models.Model):
                materiales    = request.POST.getlist('material')
                cantidades    = request.POST.getlist('cantidad')
                descripciones = request.POST.getlist('descripcion')
                unidades      = request.POST.getlist('unidad')
                for i in range(len(materiales)):
                    item=Itemsol(
                                material        =MaterialAbstracto.objects.get(nombre=materiales[i]),
                                descripcion     =descripciones[i],
                                materialReal    =None,
                                cantidad_pedida =int(cantidades[i]),
                                unidad          = unidades[i],
                                estado          ="sin asignar",
                                oc              =None,
                                solicitud       =solicitud
                                )
                    item.save()




#     material = models.ForeignKey(MaterialAbstracto, on_delete=models.CASCADE)
#     cantidad = models.IntegerField()
#     estado = models.IntegerField()
#     oc = models.ForeignKey(Odecompra, on_delete=models.CASCADE)
#     fecha       = models.DateField()
#     estado      = models.IntegerField(default=0)#0=nueva, 1=para E de compras, 2=Con O de compra
#     bodeguero   = models.ForeignKey(Profile,related_name='bodeguero', on_delete=models.CASCADE)
#     ecompra     = models.ForeignKey(Profile,related_name='ecompra', on_delete=models.CASCADE, null=True)
#     obra        = models.ForeignKey(Obra,on_delete=models.CASCADE, null=True)
#     item        = models.ManyToManyField(Itemsol)


                return render(request, 'Business/Business.html')
    else:
        raise Http404()




def VerObras(request):
    if request.method=='GET':
        obras      =   Obra.objects.order_by("nombre")
        return render(request, 'Business/VerObras.html',locals())
    else:
        raise Http404()

def Solicitudes(request):
    if (request.method=='GET'):
        solicitudes      =   Solicitud.objects()
        return render(request, 'home.html',locals())
    if (request.method=='POST'):
        return render(request, 'home.html')
    else:
        raise Http404()

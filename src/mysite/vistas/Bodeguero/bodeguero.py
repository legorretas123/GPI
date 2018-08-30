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
###############################################################################
def requiere_bodeguero(view):
    def vista_nueva(request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = Profile.objects.get(user=request.user)
            if perfil.tipo=='B':
                return view(request, *args, **kwargs)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    return vista_nueva

def VerBuzon(request):
    if request.method=='GET':
        solicitudes      =  Solicitud.objects.order_by("fecha")
        return render(request, 'Bodeguero/BodegueroBuzon.html',locals())
    else:
        raise Http404()


def VerDetalle(request,idSolicitud):
    if request.method=='GET':
        solicitud      =  Solicitud.objects.get(pk=idSolicitud)
        itemSol        = Itemsol.objects.filter(solicitud=solicitud)
        todoOK = 0
        for i in itemSol:
            if (i.estado=="sin asignar"):
                todoOK = 1
        for i in itemSol:
            if (i.estado=="encargado"):
                todoOK = 2
        return render(request, 'Bodeguero/Solicitud.html',locals())
    else:
        raise Http404()

def ItemStock(request,idItemSol):
    if request.method=='GET':
        item        = Itemsol.objects.get(pk=idItemSol)
        materiales  = MaterialReal.objects.filter(material=item.material)
        return render(request, 'Bodeguero/ItemStock.html',locals())
    else:
        raise Http404()

def ItemReservar(request,idMaterialReal,idItemSol):
    if request.method=='GET':
        itemSol         = Itemsol.objects.get(pk=idItemSol)
        materialReal    = MaterialReal.objects.get(pk=idMaterialReal)
        cantidadPedida  =itemSol.cantidad_pedida
        cantidadReal    =materialReal.cantidad
        if ((cantidadReal - cantidadPedida) >= 0):
            materialReal.cantidad=cantidadReal-cantidadPedida
            materialReal.save()
            itemSol.estado="reservado"
            itemSol.materialReal=materialReal
            itemSol.save()
        else:
            print("no podemos ejecutar esta funcion")
        solicitud      =    Solicitud.objects.get(pk=itemSol.solicitud.pk)
        itemSol        =    Itemsol.objects.filter(solicitud=solicitud)
        todoOK = 0
        for i in itemSol:
            if (i.estado=="sin asignar"):
                todoOK = 1
        for i in itemSol:
            if (i.estado=="encargado"):
                todoOK = 2
        return HttpResponseRedirect('/Item/Stock/'+str(idItemSol))
    else:
        raise Http404()



def ItemLiberar(request,idMaterialReal,idItemSol):
    if request.method=='GET':
        itemSol         = Itemsol.objects.get(pk=idItemSol)
        materialReal    = MaterialReal.objects.get(pk=idMaterialReal)
        cantidadPedida  =itemSol.cantidad_pedida
        cantidadReal    =materialReal.cantidad
        materialReal.cantidad=cantidadReal+cantidadPedida
        itemSol.estado="sin asignar"
        materialReal.save()
        itemSol.save()
        solicitud      =    Solicitud.objects.get(pk=itemSol.solicitud.pk)
        itemSol        =    Itemsol.objects.filter(solicitud=solicitud)
        todoOK = 0
        for i in itemSol:
            if (i.estado=="sin asignar"):
                todoOK = 1
        for i in itemSol:
            if (i.estado=="encargado"):
                todoOK = 2
        return HttpResponseRedirect('/Item/Stock/'+str(idItemSol))
    else:
        raise Http404()

def ItemSolicitar(request,itempk):
    if request.method=='GET':
        itemSol        = Itemsol.objects.get(pk=itempk)
        itemSol.estado="encargado"
        itemSol.save()
        return HttpResponseRedirect('/Item/Stock/'+str(itemSol.pk))
    else:
        raise Http404()

def ItemDespachar(request,idSolicitud):
    # if request.method=='GET':
    #     solicitud      =  Solicitud.objects.get(pk=idSolicitud)
    #     itemSol        = Itemsol.objects.filter(solicitud=solicitud)
    #     todoOK = 0
    #     for i in itemSol:
    #         if (i.estado=="sin asignar"):
    #             todoOK = 1
    #     for i in itemSol:
    #         if (i.estado=="encargado"):
    #             todoOK = 2
    #     return render(request, 'Bodeguero/Solicitud.html',locals())
    # else:
        raise Http404()

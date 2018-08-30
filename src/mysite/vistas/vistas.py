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

def requiere_login(view):
    def vista_nueva(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/Login/')
        return view(request, *args, **kwargs)
    return vista_nueva

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_staff:
                return render(request, 'Super/Super.html', locals())
            else:
                perfil =Profile.objects.get(user=request.user)
                if perfil.tipo == 'B':
                    return render(request, 'Bodeguero/Bodeguero.html', locals())
                if perfil.tipo == 'C':
                    return render(request, 'Business/Business.html', locals())
                if perfil.tipo == 'E':
                    return render(request, 'Encargado/Encargado.html', locals())
        else:
            return render(request, 'home.html', locals())
    else:
        raise Http404()




def Activate(request, offset):
    offset = offset
    if (request.method == 'GET'):
        try:
            perfil = Profile.objects.get(token=offset)
            form = FormularioPassword()
            return render(request, 'passwordForm.html', locals())
        except Profile.DoesNotExist:
            html = "error"
            return HttpResponse(html)
        else:
            html = "error. intente registrarse nuevamente"
            return HttpResponse(html)
    if (request.method == 'POST'):
        form = FormularioPassword(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            perfil = Profile.objects.get(token=offset)
            perfil.token=""
            perfil.activo="YES"
            usuario = User.objects.get(id=perfil.user.id)
            usuario.set_password(data['password'])
            usuario.save()
            perfil.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'passwordForm.html', {'form':form,'offset': offset})
    else:
        raise Http404()

def vista_actual_url(request):
    valor = request.META.items()
    html = []
    for k, v in valor:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

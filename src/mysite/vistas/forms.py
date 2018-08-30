from django import forms
from users.models import *
from django.contrib.auth.models import User

class FormCrearUsuario(forms.Form):
    first_name      = forms.CharField(required=True)
    last_name       = forms.CharField(required=True)
    email           = forms.CharField(required=True)
    tipo            = forms.CharField(max_length=10,widget=forms.Select(choices=ProfileType))
    telefono        = forms.CharField(required=True)

class FormCrearBodega(forms.Form):
    nombre          = forms.CharField(required=True)
    ubicacion       = forms.CharField(required=True)


class FormCrearObra(forms.Form):
    nombre              = forms.CharField(required=True)
    nombre_responsable  = forms.CharField(required=True)
    ubicacion           = forms.CharField(required=True)
    email               = forms.CharField(required=True)


class FormCrearSolicitud(forms.Form):
    obra            = forms.ModelChoiceField(queryset=Obra.objects.all(),widget=forms.Select())
    bodeguero       = forms.ModelChoiceField(queryset=Profile.objects.filter(tipo='B'),widget=forms.Select())
    # categoria       = forms.ModelChoiceField(queryset=MaterialCategoria.objects.all(),widget=forms.Select())
    material        = forms.ModelChoiceField(queryset=MaterialAbstracto.objects.all(),widget=forms.Select())
    cantidad        = forms.IntegerField(required=True)
    unidad          = forms.CharField(max_length=10,widget=forms.Select(choices=UnitType))
    descripcion     = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'descripción'}))


class FormCargarMateriales(forms.Form):
    data            = forms.FileField(required = True)
    bodega          = forms.ModelChoiceField(queryset=Bodega.objects.all())

class FormCargarProveedores(forms.Form):
    data            = forms.FileField(required = True)



class FormularioPassword(forms.Form):
    password            = forms.CharField(required=False,  widget=forms.TextInput(attrs={'placeholder': 'password'}))
    confirmPassword     = forms.CharField(required=False,  widget=forms.TextInput(attrs={'placeholder': 'confirm password'}))

class FormularioCotizacion(forms.Form):
    precio =forms.CharField(required=True,  widget=forms.TextInput(attrs={'placeholder': 'ingrese su precio sin iva..'}))
    fecha =forms.CharField(required=False,  widget=forms.TextInput(attrs={'placeholder': 'indique la fecha aproximada de entrega..'}))
    comentarios=forms.CharField(required=False,  widget=forms.TextInput(attrs={'placeholder': 'ingrese comentarios..'})) 

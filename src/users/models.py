from django.db import models
from django.contrib.auth.models import User
import string
# Create your models here.
# https://docs.djangoproject.com/en/2.0/topics/db/

# #CUENDO ESTÉ LISTO:
# 	python manage.py check
# 	python manage.py makemigrations users

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return 'images/%s/avatar.%s' % (instance.user.username,ext)

ProfileType = (
    ('B', 'Bodeguero'),
    ('E', 'Compras'),
    ('C', 'Business'),
)
UnitType = (
    ('U', 'Unidad'),
    ('M3', 'Metros cúbicos'),
    ('Kg', 'Kilogramos.'),
)
class Bodega(models.Model):
    bodega_id   = models.AutoField(primary_key=True)
    nombre      = models.CharField(max_length=100,blank=True)
    ubicacion   = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class MaterialAbstracto(models.Model):
    nombre      = models.CharField(max_length=100, primary_key=True)
    categoria   = models.CharField(max_length=100, null=True)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class MaterialCategoria(models.Model):
    categoria = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return u'{0}'.format(self.categoria)

class MaterialReal(models.Model):
    categoria = models.CharField(max_length=100, blank=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialAbstracto, on_delete=models.CASCADE)
    marca = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100, blank=True)
    caracteristicas = models.CharField(max_length=100, blank=True)
    cantidad = models.IntegerField()
    def __str__(self):
        return u'{0}'.format(self.codigo)

class Proveedor(models.Model):
    proveedor_id    = models.AutoField(primary_key=True)
    nombre          = models.CharField(max_length=100, null=True)
    email           = models.CharField(max_length=100, null=True)
    material        = models.CharField(max_length=100, null=True)
    categoria       = models.CharField(max_length=100, null=True)
    empresa         = models.CharField(max_length=100, null=True)
    telefono        = models.CharField(max_length=100, null=True)
    # material =models.ManyToManyField(MaterialReal)


class Profile(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo            = models.CharField(max_length=10, choices=ProfileType,default='')
    avatar          = models.ImageField(upload_to=upload_to, default='profileM.png')
    telefono        = models.CharField(max_length=100, null=True)
    activo          = models.CharField(max_length=4, default='NO')
    bodega          = models.ForeignKey(Bodega, on_delete=models.CASCADE, null=True, blank=True)
    token           = models.CharField(max_length=15, default="")
    def __str__(self):
        return self.user.username
class Odecompra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    ecompra = models.ForeignKey(Profile, on_delete=models.CASCADE)
    estado = models.IntegerField()

class Obra(models.Model):
    nombre              = models.CharField(max_length=100, primary_key=True)
    nombre_responsable  = models.CharField(max_length=100,default=None)
    ubicacion           = models.CharField(max_length=100)
    email               = models.CharField(max_length=100)
    def __str__(self):
        return u'{0}'.format(self.nombre)

class Solicitud(models.Model):
    fecha       = models.DateField()
    estado      = models.CharField(max_length=30)
    bodeguero   = models.ForeignKey(Profile,related_name='bodeguero', on_delete=models.CASCADE)
    ecompra     = models.ForeignKey(Profile,related_name='ecompra', on_delete=models.CASCADE, null=True)
    obra        = models.ForeignKey(Obra,on_delete=models.CASCADE, null=True)
    # fechaEstimada=models.DateField

class Itemsol(models.Model):
    material                = models.ForeignKey(MaterialAbstracto, on_delete=models.CASCADE)
    descripcion             = models.CharField(max_length=150,default=None)
    materialReal            = models.ForeignKey(MaterialReal,on_delete=models.CASCADE, null=True)
    cantidad_pedida         = models.IntegerField()
    unidad                  = models.CharField(max_length=10, choices=UnitType,default='')
    estado                  = models.CharField(max_length=30)
    oc                      = models.ForeignKey(Odecompra, on_delete=models.CASCADE,null=True)
    solicitud               = models.ForeignKey(Solicitud, on_delete=models.CASCADE,null=True)
    # prioridad     =
class Cotizacion(models.Model):
        token = models.CharField(max_length=15, primary_key=True)
        item = models.ForeignKey(Itemsol, on_delete=models.CASCADE,null=True)
        precio=models.CharField(max_length=30, default="")
        fecha=models.CharField(max_length=50, default="")
        comentarios=models.CharField(max_length=300, default="")
        respondido=models.CharField(max_length=30, default="no")
        # proveedor=models.CharField(max_length=30, default="")
        proveedor= models.ForeignKey(Proveedor, on_delete=models.CASCADE,null=True)
        def __str__(self):
            return u'{0}'.format(self.token+self.respondido)

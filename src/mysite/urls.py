from django.contrib             import admin
from django.urls                import path, re_path

from mysite.vistas              import vistas
from mysite.vistas.Super        import super
from mysite.vistas.Encargado    import encargado
from mysite.vistas.Business       import Business
from mysite.vistas.Bodeguero    import bodeguero

from django.conf                import settings
from django.conf.urls           import url
from django.conf.urls.static    import static
from django.contrib.auth.views  import login, logout

urlpatterns = [
    path('admin/',                              admin.site.urls),
    path('headers/',                            vistas.vista_actual_url),
    path('',                                    vistas.home),
    re_path(r'^Activate/([A-Z0-9]{15})/$',      vistas.Activate),
    re_path(r'^Login/$',                        login, name='login'),
    re_path(r'^Logout/$',                       logout, name='logout'),
    ##FUNCIONES DE SUPERUSUARIO
    re_path(r'^Usuarios/Crear/$',               super.requiere_staff(super.CrearUsuario)),
    re_path(r'^Usuarios/Ver/$',                 super.requiere_staff(super.VerUsuarios)),
    re_path(r'^Usuarios/Eliminar/(.+)/$',       super.requiere_staff(super.EliminarUsuario)),
    re_path(r'^Bodegas/Eliminar/(.+)/$',       super.requiere_staff(super.EliminarBodega)),
    re_path(r'^Bodegas/Crear/$',                super.requiere_staff(super.CrearBodega)),
    re_path(r'^Bodegas/Ver/$',                  super.requiere_staff(super.VerBodegas)),
    re_path(r'^Materiales/Cargar/$',            super.requiere_staff(super.CargarMateriales)),
    re_path(r'^Materiales/Ver/$',               super.requiere_staff(super.VerMateriales)),
    re_path(r'^Proveedores/Cargar/$',           super.requiere_staff(super.CargarProveedores)),
    re_path(r'^Proveedores/Ver/$',              super.requiere_staff(super.VerProveedores)),
    ##FUNCIONES DE Business DE NEGOCIOS
    re_path(r'^Obras/Ver/$',                    Business.requiere_Business(Business.VerObras)),
    re_path(r'^Obras/Crear/$',                  Business.requiere_Business(Business.CrearObra)),
    re_path(r'^Solicitudes/Crear/$',            Business.requiere_Business(Business.CrearSolicitud)),
    ##FUNCIONES DE BODEGUERO
    # re_path(r'^Solicitudes/Espera/$',         bodeguero.requiere_bodeguero(bodeguero.CrearObra)),
    # re_path(r'^Solicitudes/Listas/$',         bodeguero.requiere_bodeguero(bodeguero.CrearObra)),
    re_path(r'^Solicitudes/Buzon/$',     bodeguero.requiere_bodeguero(bodeguero.VerBuzon)),
    url(r'^Solicitudes/Detalle/(.*?)/$', bodeguero.requiere_bodeguero(bodeguero.VerDetalle), name='detallesSolicitud'),
    url(r'^Item/Stock/(.*?)/$',          bodeguero.requiere_bodeguero(bodeguero.ItemStock), name='revisarStock'),
    url(r'^Item/Reservar/(.*?)/(.*?)/$', bodeguero.requiere_bodeguero(bodeguero.ItemReservar), name='reservarItem'),
    url(r'^Item/Liberar/(.*?)/(.*?)/$',  bodeguero.requiere_bodeguero(bodeguero.ItemLiberar), name='liberarItem'),
    url(r'^Item/Solicitar/(.*?)/$',      bodeguero.requiere_bodeguero(bodeguero.ItemSolicitar), name='solicitarCompra'),
        url(r'^Item/Despachar/(.*?)/$',  bodeguero.requiere_bodeguero(bodeguero.ItemDespachar), name='despachar'),
    ##FUNCIONES DE ENCARGADO DE COMPRA
    re_path(r'^Encargos/Buzon/$',          encargado.requiere_encargado(encargado.VerBuzon), name='ComprasBuzon'),
    url(r'^Item/Cotizar/SendMail/(.*?)/$', encargado.requiere_encargado(encargado.Mail), name='CotizarSendMail'),
    url(r'^Item/Cotizar/(.*?)/$',          encargado.requiere_encargado(encargado.ItemCotizar), name='cotizarItem'),
    ##FUNCIONES DEL PROVEEDOR
    re_path(r'^Cotizar/Compra/([A-Z0-9]{15})/$',      encargado.RespuestaProveedor),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







"""
*****************************************************************************
mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

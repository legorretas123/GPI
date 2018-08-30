from django.contrib import admin

###############################
from .models import Profile
admin.site.register(Profile)
###############################
from .models import Solicitud
admin.site.register(Solicitud)
###############################
from .models import Itemsol
admin.site.register(Itemsol)
###############################
from .models import Obra
admin.site.register(Obra)
###############################
from .models import Bodega
admin.site.register(Bodega)
###############################
from .models import MaterialAbstracto
admin.site.register(MaterialAbstracto)
###############################
from .models import MaterialReal
admin.site.register(MaterialReal)
###############################
###############################
from .models import Proveedor
admin.site.register(Proveedor)
###############################
###############################
from .models import MaterialCategoria
admin.site.register(MaterialCategoria)
###############################
###############################
from .models import Cotizacion
admin.site.register(Cotizacion)

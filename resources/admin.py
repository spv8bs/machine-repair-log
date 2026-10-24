from django.contrib import admin

from resources.models import Technician, Supplier, Part

admin.site.register(Technician)
admin.site.register(Supplier)
admin.site.register(Part)

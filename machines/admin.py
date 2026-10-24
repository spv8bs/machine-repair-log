from django.contrib import admin

from machines.models import Machine, Component

admin.site.register(Machine)
admin.site.register(Component)

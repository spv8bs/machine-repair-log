from django.contrib import admin

from repairs.models import Repair, RepairAction

@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('machine', 'component', 'detected_on', 'limited_on', 'resolved_on')
    list_filter = ('machine',)

admin.site.register(RepairAction)
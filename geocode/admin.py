from django.contrib import admin
from geocode.models import Project, Record

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    #inlines = [FieldInline,ProjectionOptionInline,ShapeFileMatcheInline]
    list_display = ("name", "user","history_line","finish_input_data")
    readonly_fields=('finish_input_data',)
    list_filter = ('user',)

    def save_model(self, request, task, form, change):
        if task.user == None:
           task.user = request.user
           task.save()
        else:
           task.save()

admin.site.register(Project, ProjectAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_display = ("address_id", "street", "ignore_street", "city", "ignore_city", "state","ignore_state","zip","geo_score","geo_address","geo_lat","geo_lon","resource","flag")
    
admin.site.register(Record, RecordAdmin)

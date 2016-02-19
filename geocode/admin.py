from django.contrib import admin
from geocode.models import Project, Address, ApiKey, ApiKeyAcceptValue,ProjectField

class ApiKeyAcceptValueInline(admin.TabularInline):
    model = ApiKeyAcceptValue

class ProjectFieldInline(admin.TabularInline):
    model = ProjectField

# Register your models here.
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "key")
    inlines = [ApiKeyAcceptValueInline]
admin.site.register(ApiKey, ApiKeyAdmin)

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectFieldInline]#ProjectionOptionInline,ShapeFileMatcheInline]
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

class AddressAdmin(admin.ModelAdmin):
    list_display = ("address_id", "street", "ignore_street", "city", "ignore_city", "state","ignore_state","zip","geo_score","geo_address","geo_lat","geo_lon","resource","flag")
    
admin.site.register(Address, AddressAdmin)

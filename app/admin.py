from django.contrib import admin
from .models import (
    Customer, Measurement, Hinge, DoorModel, 
    ColorCombination, GlassType, Door, Lock, 
    Finish, DoorOpen, Frame
)

# Admin classes for each model to display all fields in the list view
class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]

class MeasurementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Measurement._meta.fields]

class HingeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Hinge._meta.fields]

class DoorModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DoorModel._meta.fields]

class ColorCombinationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ColorCombination._meta.fields]

class GlassTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GlassType._meta.fields]

class DoorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Door._meta.fields]

class LockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lock._meta.fields]

class FinishAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Finish._meta.fields]

class DoorOpenAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DoorOpen._meta.fields]

class FrameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Frame._meta.fields]

# Registering models with their corresponding admin classes
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Hinge, HingeAdmin)
admin.site.register(DoorModel, DoorModelAdmin)
admin.site.register(ColorCombination, ColorCombinationAdmin)
admin.site.register(GlassType, GlassTypeAdmin)
admin.site.register(Door, DoorAdmin)
admin.site.register(Lock, LockAdmin)
admin.site.register(Finish, FinishAdmin)
admin.site.register(DoorOpen, DoorOpenAdmin)
admin.site.register(Frame, FrameAdmin)

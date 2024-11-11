from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, PatientToken, AvailableTime


admin.site.site_header = 'Heednheal Admin Panel'


class GroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
    

class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'name', 'department', 'user_permissions', 'is_active', 'is_staff')

    def has_change_permission(self, request, obj=None):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True
        # If not a superuser, restrict changing permissions
        return False
    
    def has_add_permission(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True
        # If not a superuser, restrict adding permissions
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(username=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data and form.cleaned_data['password']:
            obj.set_password(form.cleaned_data['password'])
        obj.save()
    

class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'available_date', 'available_time', 'token_count')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(doctor=request.user)
        return qs


class PatientTokenAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'name', 'phone_no', 'token_no', 'date', 'time')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(doctor=request.user)
        return qs


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PatientToken, PatientTokenAdmin)
admin.site.register(AvailableTime, AvailableTimeAdmin)
from django.contrib import admin
from kunder.models import Customer, Delivery, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserAdminInline (admin.TabularInline):
    model = User

class CustomerAdmin (admin.ModelAdmin):
    list_display =('full_name','full_adress', 'phone', 'active')
    #ordering = ('full_name',)
    search_fields = ('first_name', 'last_name', 'phone')
    list_filter = ('active',)
    fields = (('first_name', 'last_name'),
                ('street', 'postal_code', 'city'),
                ('week_0', 'week_1'),
                ('email',),
                ('phone',),
                ('cancels'))
                
    filter_horizontal = ('cancels',)
admin.site.register(Customer, CustomerAdmin)

class DeliveryAdmin (admin.ModelAdmin):
    pass

admin.site.register(Delivery, DeliveryAdmin)




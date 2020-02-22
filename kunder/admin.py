from django.contrib import admin
from kunder.models import Customer, Delivery, User
from django.contrib.auth.admin import UserAdmin

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
    def formfield_for_manytomany(self, db_field, request, **kwargs):

        # TODO: Perhaps an ugly hack. Using the url hardcoded.
        object_id = int([i for i in str(request.path).split('/') if i][-2])
        
        if db_field.name == "cancels":
            pass
            kwargs["queryset"] = Customer.objects.get(pk=object_id).upcomming_deliveries_including_canceled()
        return super(CustomerAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Customer, CustomerAdmin)

class DeliveryAdmin (admin.ModelAdmin):
    pass

admin.site.register(Delivery, DeliveryAdmin)




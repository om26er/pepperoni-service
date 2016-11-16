from django.contrib import admin
from django.contrib.auth.models import Group

from pepper.models import Restaurant


class RestaurantAdminProxy(Restaurant):
    class Meta:
        verbose_name = 'Restaurant Pending Approval'
        verbose_name_plural = 'Restaurants Pending Approval'
        proxy = True


class RestaurantAdmin(admin.ModelAdmin):
    readonly_fields = (
        'rating',
        'menu',
        'owner_contact',
        'owner_name',
        'closing_time',
        'opening_time',
        'contact',
        'name',
        'location',
    )

    class Meta:
        model = Restaurant

    def get_queryset(self, request):
        return self.model.objects.filter(approved=True)


class RestaurantNeedApprovalAdmin(admin.ModelAdmin):
    readonly_fields = (
        'rating',
        'menu',
        'owner_contact',
        'owner_name',
        'closing_time',
        'opening_time',
        'contact',
        'name',
        'location',
    )

    class Meta:
        model = RestaurantAdminProxy

    def get_queryset(self, request):
        return self.model.objects.filter(approved=False)

    def has_add_permission(self, request):
        return False


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestaurantAdminProxy, RestaurantNeedApprovalAdmin)
admin.site.unregister(Group)

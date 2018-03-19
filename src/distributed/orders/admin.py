from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from distributed.orders.models import Order
from distributed.orders import signals


def delete_objects(modeladmin, request, queryset):
    for obj in queryset:
        modeladmin.delete_model(request, obj)

delete_objects.short_description = delete_selected.short_description


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    actions = [delete_objects]

    def get_actions(self, request):
        actions = super(OrderAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def log_addition(self, request, object, message):
        log = super(OrderAdmin, self).log_addition(request, object, message)
        signals.created.send(sender=self.__class__, id=object.id, name=object.name, number=object.number)

        return log

    def log_change(self, request, object, message):
        log = super(OrderAdmin, self).log_change(request, object, message)
        signals.updated.send(sender=self.__class__, id=object.id, name=object.name,number=object.number)

        return log

    def delete_model(self, request, obj):
        id = obj.id
        super(OrderAdmin, self).delete_model(request, obj)
        signals.deleted.send(sender=self.__class__, id=id)

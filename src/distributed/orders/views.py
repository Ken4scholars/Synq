from rest_framework import viewsets
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer
from . import signals


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def _is_sync(self):
        return settings.DJANGO_SYNC_HEADER in self.request.META and \
               self.request.META[settings.DJANGO_SYNC_HEADER] == settings.SYNC_HEADER_VALUE

    def perform_create(self, serializer):
        instance = serializer.save()
        if not self._is_sync():
            signals.created.send(sender=self.__class__, id=instance.id, name=instance.name, number=instance.number)

    def perform_update(self, serializer):
        instance = serializer.save()
        if not self._is_sync():
            signals.updated.send(sender=self.__class__, id=instance.id, name=instance.name, number=instance.number)

    def perform_destroy(self, instance):
        id = instance.id
        super(OrderViewSet, self).perform_destroy(instance)
        if not self._is_sync():
            signals.deleted.send(sender=self.__class__, id=id)

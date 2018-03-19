from django.db import models


class Order(models.Model):
    number = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100, unique=False)

    class Meta:
        ordering = ('number',)




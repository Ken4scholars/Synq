import django.dispatch

created = django.dispatch.Signal(providing_args=['id', 'number', 'name', 'created'])

deleted = django.dispatch.Signal(providing_args=['id'])

updated = django.dispatch.Signal(providing_args=['id', 'number', 'name', 'modified'])

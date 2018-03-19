from rest_framework import routers

from . import views

app_name = 'orders'

router = routers.SimpleRouter()
router.register(r'', views.OrderViewSet, base_name='orders')

urlpatterns = router.urls

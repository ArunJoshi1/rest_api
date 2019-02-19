from django.contrib import admin
from django.urls import path,include
from core.views import Customer,Professionviewset,Datasheetviewset,Document
from rest_framework import routers
from rest_framework.authtoken.views import  obtain_auth_token


# api routers
router = routers.DefaultRouter()
router.register('customers',Customer,basename='customer')
router.register('profession',Professionviewset,basename='profession')
router.register('datasheet',Datasheetviewset,basename='datasheet')
router.register('document',Document,basename='document')





# django urls

urlpatterns = [
    path('api/',include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path(r'api-token-auth/', obtain_auth_token),
]

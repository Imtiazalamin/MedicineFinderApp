from django.contrib import admin
from LocalMedicineFinderapp import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import Pharmacy_viewset, stock_viewset, medicine_viewset


router = DefaultRouter()
router.register("pharmacies", Pharmacy_viewset, basename="pharmacy")
router.register("stocks", stock_viewset, basename="stock")
router.register("medicines", medicine_viewset, basename="medicine")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)), # register er jonno ei line  
   
 
]

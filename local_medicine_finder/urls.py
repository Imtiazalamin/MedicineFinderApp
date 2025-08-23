from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from LocalMedicineFinderapp import views

router = DefaultRouter()
router.register('register', views.medicine_model_view_set, basename='register')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('LocalMedicineFinderapp.urls')),  # এখানেই সব app router URLs include হবে
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

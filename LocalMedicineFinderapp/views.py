from django.shortcuts import render
from .models import CustomUserRegister, Pharmacy, Medicine, stock, Whishlist
from rest_framework import viewsets, status, permissions, filters # modelviewset use korar jonno
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response # api theke response return korar jonno
from .serializers import UserRegistrationSerializer, Pharmacyserializer, Medicineserializer, stockserializer, WishListserializer #  .seriliazers theke UserRegistrationSerializer theke data anlam
from rest_framework.permissions import  AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .filters import StockFilter





class medicine_model_view_set(viewsets.ModelViewSet):
   # registration system
    queryset = CustomUserRegister.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'user create successfully'}, status=status.HTTP_201_CREATED)

# Pharmacy Viewset (ঠিক আছে)
class Pharmacy_viewset(viewsets.ModelViewSet):
    serializer_class = Pharmacyserializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'address']

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'seller':
            return Pharmacy.objects.filter(owner=user)
        return Pharmacy.objects.all()  

    def perform_create(self, serializer):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can create")
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can update")
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("You can only update your own data")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can delete")
        if instance.owner != self.request.user:
            raise PermissionDenied("You can only delete your own data")
        instance.delete()


# Stock Viewset (fixed)
class stock_viewset(viewsets.ModelViewSet):
    serializer_class = stockserializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'seller':
            return stock.objects.filter(pharmacy__owner=user)
        return stock.objects.all()

    def perform_create(self, serializer):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can create")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can update")
        if serializer.instance.pharmacy.owner != self.request.user:
            raise PermissionDenied("You can only update your own data")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can delete")
        if instance.pharmacy.owner != self.request.user:
            raise PermissionDenied("You can only delete your own data")
        instance.delete()


# Medicine Viewset (fixed)
class medicine_viewset(viewsets.ModelViewSet):
    serializer_class = Medicineserializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['medicine_name', 'company_name', 'cetagory']

    def get_queryset(self):
        return Medicine.objects.all()

    def perform_create(self, serializer):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can create medicine")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can update medicine")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can delete medicine")
        instance.delete()

    # DELETE only for seller & owner
    def perform_destroy(self, instance):
        if self.request.user.user_type != 'seller':
            raise PermissionDenied("Only sellers can delete")
        if instance.owner != self.request.user:
            raise PermissionDenied("You can only delete your own data")
        instance.delete()
  

class WhishlistViewset(viewsets.ModelViewSet):
    queryset = Whishlist.objects.all()
    serializer_class = WishListserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Whishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'buyer':
            raise PermissionDenied("only buyer add whishlist")
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user.user_type != 'buyer':
            raise PermissionDenied('only can buyer delete wishlist')
        if instance.user != self.request.user:
            raise PermissionDenied('you can delete only your whishlist')
        instance.delete()






      
    
        
           
    




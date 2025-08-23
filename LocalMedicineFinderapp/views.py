from django.shortcuts import render
from .models import CustomUserRegister, Pharmacy, Medicine, stock
from rest_framework import viewsets, status, permissions # modelviewset use korar jonno
from rest_framework.response import Response # api theke response return korar jonno
from .serializers import UserRegistrationSerializer, Pharmacyserializer, Medicineserializer, stockserializer #  .seriliazers theke UserRegistrationSerializer theke data anlam
from rest_framework.permissions import IsAuthenticated, AllowAny




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
    
class Pharmacy_viewset(viewsets.ModelViewSet):
    serializer_class = Pharmacyserializer
    permission_classes = [permissions.IsAuthenticated] # login user lagbe login chara parbe na
    # buyer seller alada korlam 
    def get_queryset(self):
        if self.request.user.user_type == 'seller':
            return Pharmacy.objects.filter(owner=self.request.user) # jodi user seller hoi tahole she onumorti pabe
        # buyer pabe na
        return Pharmacy.objects.none() 

class stock_viewset(viewsets.ModelViewSet):
    serializer_class = stockserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # শুধু সেই stock আসবে যেগুলো current user এর pharmacy এর সাথে লিঙ্কড
        return stock.objects.filter(pharmacy_owner=self.request.user)
    
    def perform_create(self, serializer):
        # pharmacy id frontend theke nibo
        pharmacy_id = self.request.data.get('pharmacy')
        # ebar id diya pharmacy ber korbo
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        # abar check korbo eta ki pharmacy er oi user ki na
        if pharmacy.owner != self.request.user:
            raise PermissionError('you can only add your stock own pharmacy')
        
        serializer.save(pharmacy=pharmacy) #  stock save korlam

class medicine_viewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = Medicineserializer
    queryset = Medicine.objects.all()

    def get_queryset(self):
        return Medicine.objects.all() # shob medicine diya shuru hobe
        # query parameter the nam r city nilam
        name = self.request.query_params.get('name')
        city = self.request.query_params.get('city')

        # jodi name thake name diya filter korbo
        if name:
             queryset = queryset.filter(name__icontains=name)

        # jodi city thake city diya filter korbo  
        if city:
            queryset = queryset.filter(stock__pharmacy__city__icontains=city).distinct()

        return queryset    






      
    
        
           
    




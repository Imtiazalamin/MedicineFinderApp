from rest_framework import serializers
from .models import CustomUserRegister, Pharmacy, Medicine, stock, Whishlist
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUserRegister
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'phone_number', 'address', 'user_type'] 
        extra_kwargs = {'password': {'write_only': True}} 

    # serializer valiaton er jonno confirm_passwor use korle ata dite hobe
    def Validated(self, attrs):
        if attrs['password'] != attrs['confirm_password']: # jodi pass1 pass2 na mile
            raise serializers.ValidationError({'pasword': 'password must match'}) # pass1 pass2 match na hoile ei error dibe
        return attrs # shob thik thakle validated data return
    
    # notun user create korar jonno   
    def create(self, validated_data):
         validated_data.pop('confirm_password')#create hoar por pass2 dorkar nei tai cut korlm
         password = validated_data.pop('password') # password alada kore rakhlam jeno pore bebohar kora jai
         user = self.Meta.model(**validated_data)
         user.set_password(password) # pass ke set kora hoi pass hishabe text hishabe na
         user.save()
         return user
    

# jwt authenticatin akhane banabo
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True) 
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("You must register first or check credentials") 


class Pharmacyserializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy  
        fields = ['id', 'name', 'address', 'city', 'lat', 'lng', 'image']
        read_only_fields = ['owner'] 


class Medicineserializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'medicine_name', 'description', 'cetagory', 'company_name', 'price' 'image']
        read_only_fields = ['owner'] # owner শুধু দেখা যাবে, client সেট করতে পারবে না

class stockserializer(serializers.ModelSerializer):
    class Meta:
        model = stock
        fields = ['id', 'pharmacy', 'medicine_name', 'quantity', 'price'] 
        read_only_fields = ['owner']       


class WishListserializer(serializers.ModelSerializer):
    class Meta:
        model = Whishlist
        fields= ['id', 'user', 'medicine', 'create_at'] 
        read_only_fields = ['user', 'created_at']      



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserRegister
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address']
        read_only_fields = ['id', 'username', 'email']  # শুধু update হবে কিছু ফিল্ড


       
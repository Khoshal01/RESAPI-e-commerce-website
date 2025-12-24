from rest_framework import serializers
from django.contrib.auth.models import User , Group
from django.contrib.auth.password_validation import validate_password
from home.models import ProductModel  , OrderModel


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length =50)
    email = serializers.EmailField(required = True)
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )
    password2 = serializers.CharField(write_only = True , required = True )

    class Meta:
        model = User 
        fields = ['username','email','password','password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already in use"})
        
        return attrs
    




class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 50)
    email  = serializers.EmailField()
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )
    password2 = serializers.CharField(write_only = True , required = True )
    role = serializers.CharField()

    def validate(self, data):
        role = data['role'].lower()
        if role not in ['customer', 'owner']:
            raise serializers.ValidationError('Invalid role')
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username Already exists')
        
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Email Already used,Try with different email.')
        
        return data 
    
    def create(self,data):
        data.pop('password2')
        role = data['role'].lower()
        data.pop('role')
        try:
            user = User.objects.create_user(username = data['username'],email = data['email'])
            user.set_password(data['password'])
            user.save()

            group = Group.objects.get(name=role)
            user.groups.add(group)
            
        except Exception :
            raise serializers.ValidationError('Your data did no save,try again!')

        return user 

    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        exclude = ['owner','image']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        exclude = ['orderowner']
        read_only_fields = ['customer']

    def validate(self, validated_data):
    
        if not ProductModel.objects.filter(product_name=validated_data['orderproduct_name']).exists():
            raise serializers.ValidationError({"orderproduct_name": "No product with this name"})

        valid_statuses = [choice[0] for choice in OrderModel.STATUS_CHOICES]
        if validated_data['status'] not in valid_statuses:
            raise serializers.ValidationError({"status": f"Invalid status, must be one of {valid_statuses}"})

        return validated_data
    





    
            
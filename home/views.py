from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated  
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token 
from django.conf import settings
from home.serializer import RegisterSerializer , ProductSerializer , OrderSerializer
from home.models import ProductModel , OrderModel
from rest_framework import status, viewsets
from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.core.paginator import Paginator 
from rest_framework.pagination import PageNumberPagination



class ObjectPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class loginAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username = username,password = password)
        print(user)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)
        
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access_token": str(refresh.access_token),
        })
    


class RegistrationAPI(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            role = request.data.get('role', 'Customer')  # default to Customer
            if role == 'Owner':
                group = Group.objects.get(name='Owner')
            else:
                group = Group.objects.get(name='Customer')
            user.groups.add(group)

            return Response({
                'message': 'User created successfully!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role':f"User created and assigned to {role} group"
            }, status=status.HTTP_201_CREATED)
        
        
        
        # Returns detailed error messages for each field
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProductModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class  = ProductSerializer
    pagination_class  = ObjectPagination

    def get_queryset(self):
        
        return ProductModel.objects.filter(owner = self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(owner = self.request.user)

        
    
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get_queryset(self):
        user = self.request.user

        # 🔹 OWNER: see orders for products he owns
        if user.groups.filter(name='owner').exists():
            products = ProductModel.objects.filter(owner=user)
            return OrderModel.objects.filter(
                orderproduct_name__in=products
            ).distinct()

    # CUSTOMER
        if user.groups.filter(name='customer').exists():
            return OrderModel.objects.filter(orderowner=user)

        return OrderModel.objects.none()

       
        
    def perform_create(self,serializer):
        user = self.request.user

        if  user.groups.filter(name='owner').exists():
            raise PermissionError('Only Customer can create order')
        serializer.save(orderowner = user)
    
    


     
    

    


        

            



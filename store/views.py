from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers

from store.serializers import UserSerializer,ProductSerializer,BasketItemSerializer,BasketSerializer
from store.models import Product,Basket,BasketItem

class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class ProductsView(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    #  url:http://127.0.0.1:8000/api/products/{id}/add_to_basket
    # custom method for adding to basket even though this is product view
    @action(methods=['post'],detail=True)
    def add_to_basket(self,request,*args,**kwargs):
        product_id=kwargs.get('pk')
        product_object=Product.objects.get(id=product_id)
        #checking whose basket it is
        basket_object=request.user.cart
        basket_product=request.user.cart.cartitem.all().values_list('product',flat=True)
        print(basket_product)
        #Already added product doesn't need to be add again to that user's basketitem, instead quantity can be incresed by how much adding second/muliptle times
        if int(product_id) in basket_product:
            basket_item_object=BasketItem.objects.get(basket=basket_object,product__id=product_id)
            basket_item_object.quantity+=int(request.data.get('quantity',1)) #if quantites is not passed, let default qty be 1
            print(basket_item_object.quantity)
            basket_item_object.save()
            serializer=BasketItemSerializer(basket_item_object)
            return Response(data=serializer.data)
        
        serializer=BasketItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(basket=basket_object,product=product_object)
            return Response(data=serializer.data)
           
        else:
            return Response(data=serializer.errors)
        
           
            
        
    # this productview is made for customers, so cusomter shouldn't have permission to create,update,destroy products
    # overriding/blocking default def create,update,destory in ModelViewSet()
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied')
    
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied')
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError('Permission Denied')
    

class BasketView(viewsets.ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list(self,request,*args,**kwargs):
        qs=request.user.cart
        deserializer=BasketSerializer(qs,many=False)
        return Response(data=deserializer.data)
        
    
class BasketItemView(viewsets.ModelViewSet):
    serializer_class=BasketItemSerializer
    queryset=BasketItem.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    #only owner of basket should be able to update/delete/take detail of their respective basket item
    #so we check whether token user is the owner of that basket
    def perform_update(self, serializer):
        user=self.request.user #token sending user
        owner=self.get_object().basket.owner  #get_object() gives the current basketitem with ID given in url
        if user==owner:
            return super().perform_update(serializer) #theier default method
        else:
            raise serializers.ValidationError('Owner Permission Required!')
        
    def perform_destroy(self, instance):
        user=self.request.user #token sending user
        owner=self.get_object().basket.owner  #get_object() gives the current basketitem with ID given in url
        if user==owner:
            return super().perform_destroy(instance)
        else:
            raise serializers.ValidationError('Owner Permission Required ***!')
        
    
        

    def retrieve(self, request, *args, **kwargs):
        user=self.request.user
        owner=self.get_object().basket.owner 
        if user==owner:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            raise serializers.ValidationError('Owner Permission Required!')
        


    def create(self, request, *args, **kwargs):#this is already done in Product View, to add items to baskteitems
        raise serializers.ValidationError('Permission denined')
    
    def list(self, request, *args, **kwargs):  #list is blocked since, we don't want to see every user's basketitems,also we can see logged user's cart Basketview
        raise serializers.ValidationError('Permission denined')



        


    

    
        
    

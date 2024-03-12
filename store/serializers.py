from django.contrib.auth.models import User

from rest_framework import serializers

from store.models import Product,BasketItem,Basket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']
        read_only_fields=['id']


    def create(self, validated_data):
        return User.objects.create_user(**validated_data) #for encryption
    

class ProductSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    class Meta:
        model=Product
        fields='__all__'


class BasketItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True) #nested serializer
    total_product_price=serializers.IntegerField(read_only=True) #from model
    class Meta:
        model=BasketItem
        fields='__all__'
        read_only_fields=['id','basket','product','created_at','updated_at','is_active','total_product_price']


class BasketSerializer(serializers.ModelSerializer):
    cart_items=BasketItemSerializer(read_only=True,many=True) #deserialization is done here #cart_item from models property with fn
    cart_item_quantity=serializers.CharField(read_only=True) #from model
    subtotal_price=serializers.IntegerField(read_only=True)
    class Meta:
        model=Basket
        fields=['id','owner','created_at','updated_at','is_active','cart_items','cart_item_quantity','subtotal_price']

    
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",default="default.jpg")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_trending=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property   #@property is given call cart_items fn everywhere like owner,
    def cart_items(self):
        #qs=BasketItem.objects.filter(basket=self)  use this incase you forgot to give relatedname 'cartitem'
        return self.cartitem.all()
    
    @property
    def cart_item_quantity(self):
        qs=self.cart_items
        return qs.count()
    
    @property
    def subtotal_price(self):
        basket_items=self.cart_items #method calling in . self.cartitem.all(), since property dec, we don't have to call self.cartitems()
        total_sum=0
        if basket_items:
            total_sum=sum([item.total_product_price for item in basket_items])
        
        return total_sum
    
class BasketItem(models.Model):
    basket=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property          #to get price of product with quantity
    def total_product_price(self):
        return self.quantity*self.product.price




#function creating- when a user creates an account in User Model, automatically creates a Bastket instance/object for him/her

def create_basket(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)

post_save.connect(create_basket,sender=User)

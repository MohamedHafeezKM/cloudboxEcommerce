from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

from store import views


router=DefaultRouter()

router.register('products',views.ProductsView,basename='products')
router.register('baskets',views.BasketView,basename='baskets')
router.register('baskets/item',views.BasketItemView,basename='basketitem')
urlpatterns = [
    path('register/',views.SignUpView.as_view()),
    path('generate-token/',ObtainAuthToken.as_view()),
    
]+router.urls

from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('signup/',views.signup),

    path('update_item/',views.updateItem,name='update_item'), #this is json response
    path('process_order/',views.processOrder,name='process_order'), #this is json response
     path('accounts/',include('django.contrib.auth.urls')),
]
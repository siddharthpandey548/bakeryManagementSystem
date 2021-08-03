from django.urls import path
from . import views

urlpatterns=[
    path('',views.index , name='index'),
    path('register',views.register , name='register'),
    path('login',views.login , name='login'),
    path("logout",views.logout,name="logout"),
    path('product',views.product , name='product'),
    path('checkout',views.checkout , name='checkout'),
    path("get_cart_data",views.get_cart_data,name="get_cart_data"), 
    path("change_quan",views.change_quan,name="change_quan"),
    path("process_payment",views.process_payment,name="process_payment"),
    path("payment_done",views.payment_done,name="payment_done"),
    path("payment_cancelled",views.payment_cancelled,name="payment_cancelled"),
    path("contact",views.contactus,name="cnt"),
]
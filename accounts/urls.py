from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('products/',views.products,name="products"),
    path('customers/<str:pk>/',views.customer,name="customers"),
    path('create_customers/',views.createCustomer,name="create_customer"),
    #Orders
    path('create_order/<str:pk>/',views.createOrder,name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    #User authentication
    path('register/',views.register_user,name="registerUser"),
    path('login/',views.login_user,name="loginUser"),
    path('logout/',views.logout_user,name="logoutUser"),
]
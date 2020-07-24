from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


# Create your views here.
@login_required(login_url = 'loginUser')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status ='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending

    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url = 'loginUser')
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url = 'loginUser')
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    order_count = orders.count()

    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count
    }
    return render(request,'accounts/customer.html',context)

@login_required(login_url = 'loginUser')
def createCustomer(request):
    form = CreateCustomerForm()
    context = {'form':form}

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')

    return render(request,'accounts/create_customer.html',context)

#Orders
@login_required(login_url = 'loginUser')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields = ('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid:
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url = 'loginUser')
def updateOrder(request,pk): 

    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url = 'loginUser')
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request,'accounts/confirm_delete.html',{'order':order})


#User Authentication

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegisterUserForm()
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'User Created')
                return redirect('/login')
        context = {'form':form}
        return render(request,'accounts/register.html',context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username ,password = password)

            if user is not None:
                login(request,user)
                messages.success(request,'User Logged in')
                return redirect('home')
            else:
                messages.success(request,'Username or password is incorrect')

        return render(request,'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('loginUser')
    
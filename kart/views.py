from http.client import HTTPResponse
import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from  shop.form import CustomUserForm
from .models import Catagory,Product,Cart,Favour
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home(request):
    products = Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{'products':products})

def fav_page(request):
    if request.headers.get('X-Requested-with')=='XMLHttpResponse':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            #print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favour.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favourite'},status=200)
                else:
                        Favour.objects.create(user=request.user,product_id=product_id)  
                        return JsonResponse({'status':'Product Added to Favourite'},status=200)    
        else:
            return JsonResponse({'status':'Login to add Favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def fav_view_page(request):
    if request.user.is_authenticated:
        fav = Favour.objects.filter(user = request.user)
        return render(request,"shop/fav.html",{'fav':fav})
    else:
        return redirect('/')   

def remove_cart(request,cid):
    cart_item = Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect('/cart')    

def remove_fav(request,fid):
    item = Favour.objects.get(id=fid)
    item.delete()
    return redirect('fav_view_page')     


def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        return render(request,"shop/cart.html",{'cart':cart})
    else:
        return redirect('/')

def add_to_cart(request):
    if request.headers.get('X-Requested-with')=='XMLHttpResponse':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)  
                        return JsonResponse({'status':'Product Added to Cart'},status=200)  
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)    
        else:
            return JsonResponse({'status':'Login to add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logout successfully")
        return redirect('/')    


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:    
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name, password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged successfully")
                return redirect('/')
            else:
                  messages.error(request,"Invalid username or password")   
                  return redirect('/login') 
        return render(request,"shop/login.html")

def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form =CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration successfully completed you can login now...")
            return redirect('/login')
    return render(request,"shop/register.html",{"form":form})   

def collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,"shop/collection.html",{'catagory':catagory})    

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(Catagory__name=name)
        catagory = Catagory.objects.filter(name=name).first()
        return render(request,"products/index.html",{'products':products,'catagory':catagory})  
    else:
        messages.warning(request,'No Such Catagory Found')
        return redirect('collections')

def product_view(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname, status=0)):
            products = Product.objects.filter(name=pname,status=0).first()
            return render(request,"products/product_view.html",{'products':products})    
        else:
            messages.warning(request,'product is not found')

    else:
        messages.warning(request,"catagory is not found")
        return redirect ('collections')  
    

    
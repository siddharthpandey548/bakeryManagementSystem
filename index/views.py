from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,auth
from . models import products,Category,Register,cart,Order
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings 

# Create your views here.
def register(request):     
    if request.method=="POST":
        fname = request.POST["fir"]
        last = request.POST["las"]
        un = request.POST["usr"]
        pwd = request.POST["pass"]
        cpwd = request.POST["cnf"]
        em = request.POST["mail"]
        con = request.POST["num"]
        if(pwd==cpwd):
            if User.objects.filter(username=un).exists():
                messages.info(request,"username taken")
                return redirect("register")
            elif User.objects.filter(email=em).exists():
                messages.info(request,"email taken")
                return redirect("register")
    
       
        
        us=User.objects.create_user(first_name=fname,last_name=last,username=un,email=em,password=pwd)
        us.save() 
        
        us2=Register(user=us,mobileno=con)
        us2.save()
        return render(request,"login.html",{"status":"Mr/Miss. {} your Account created Successfully".format(fname)})
    return render(request,"login-register.html")

def login(request):
    if(request.method=="POST"):

        username=request.POST['username']
        password=request.POST['password']
        

        user=auth.authenticate(username=username,password=password)
        if user != None:
            auth.login(request,user)
            return redirect('index')
        else:
              messages.info(request,"not matching")
              return redirect('login')
            


    else:
        return render(request,"login.html")
def logout(request):
    auth.logout(request)
    return redirect('index') 




      
def index(request):
    context = {}
    catsts = Category.objects.all().order_by("cat_name")
    context["category"] = cats
    prod = products.objects.all().order_by("name")
    context["products"] = prod
    
    

    return render(request,"product.html",context)
def checkout(request):
    context={}
    items = cart.objects.filter(user__id=request.user.id,status=False)
    context["items"] = items
    if request.user.is_authenticated:
        if request.method=="POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"] 
            is_exist = cart.objects.filter(product__id=pid,user__id=request.user.id,status=False)
            if len(is_exist)>0:
                context["msz"] = "Item Already Exists in Your Cart"
                context["cls"] = "alert alert-warning"
            else:    
                product=get_object_or_404(products,id=pid)
                usr = get_object_or_404(User,id=request.user.id)
                c = cart(user=usr,product=product,quantity=qty)
                c.save()
                context["msz"] = "{} Added in Your Cart".format(product.name)
                context["cls"] = "alert alert-success"


        
    
    else:
        context["status"] = "Please Login First to View Your Cart"
    return render(request ,"cart.html",context)

    
def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id, status=False)
    sale,quantity =0,0
    for i in items:
        sale += float(i.product.price)*i.quantity
        
        quantity+= float(i.quantity)

    res = {
        "offer":sale,"quan":quantity,
    }
    return JsonResponse(res)
    
def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

def process_payment(request):
    items = cart.objects.filter(user_id__id=request.user.id,status=False)
    products=""
    amt=0
    inv = "INV10001-"
    cart_ids = ""
    p_ids =""
    for j in items:
        products += str(j.product.name)+"\n"
        p_ids += str(j.product.id)+","
        amt += float(j.product.price)
        inv +=  str(j.id)
        cart_ids += str(j.id)+","

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': products,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           ('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           ('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              ('payment_cancelled')),
    }
    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session["order_id"] = ord.id
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'checkout.html', {'form': form})

def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order,id=order_id)
        ord_obj.status=True
        ord_obj.save()
        
        for i in ord_obj.cart_ids.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
    return render(request,"payment_success.html")

def payment_cancelled(request):
    return render(request,"payment_failed.html")

def contactus(request):
    return render(request,"contact.html")
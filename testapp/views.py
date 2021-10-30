from django.shortcuts import render,redirect
import io
from django.db import connection
from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from .models import User, Sales,Product,OrderProduct,Followupnotes
from .form import Usersignupform
from django.conf import settings 
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template 
from django.template import Context
from django.http import HttpResponse
import json
from django.http import JsonResponse
from io import BytesIO
from xhtml2pdf import pisa
from email.message import EmailMessage
from django.contrib.auth.models import  Group
from django.db import connections
from datetime import date
def home(request):
    if request.user.is_authenticated:
        collection_perm = User.objects.filter(pk=request.user.id, groups__name='collection').exists()
        sales_perm = User.objects.filter(pk=request.user.id, groups__name='sales').exists()
        return render(request,'index.html',{'user_perm':collection_perm,'sales_perm':sales_perm})
    else:
        return redirect('/login')



def create_sales(request):
    if request.user.is_authenticated and  User.objects.filter(pk=request.user.id, groups__name='sales').exists():
        collection_perm = User.objects.filter(pk=request.user.id, groups__name='collection').exists()
        sales_perm = User.objects.filter(pk=request.user.id, groups__name='sales').exists()
        all_product = Product.objects.all()
        itemid   = []
        itemname = []
        totalprice = 0
        for i in all_product:
            itemid.append(i.id)
            itemname.append(i.item)
        mylist = zip(itemid, itemname)

        user = request.user.first_name +request.user.last_name
        if request.method=="POST":
            context_list = []
            data=User.objects.get(id=request.user.id)

            sales = Sales(
                b_firmname    = request.POST['b_firm'],
                b_addr1       = request.POST['b_address'],
                b_addr2       = request.POST['b_address2'],
                b_city        = request.POST['b_city'],
                b_state       = request.POST['b_state'],
                b_zip         = request.POST['b_zip'],
                b_country     = request.POST['b_country'],
                s_firmname    = request.POST['s_firm'],
                s_addr1       = request.POST['s_address'],
                s_addr2       = request.POST['s_address2'],
                s_city        = request.POST['s_city'],
                s_state       = request.POST['s_state'],
                s_zip         = request.POST['s_zip'],
                s_country     = request.POST['s_country'],
                b_date        = request.POST['date'],
                b_buyer       = request.POST['buyer'],
                b_purchase_order= request.POST['purchase_order'],
                b_tirms       = request.POST['terms'],
                contact1      = request.POST['main_tel'],
                contact2      = request.POST['alt_tel'],
                email         = request.POST['email'],
                created_by    = data
            )
            #a =sales.save()

            sales_id  = Sales.objects.latest('id')

            qty               = request.POST.getlist('qty[]')
            item              = request.POST.getlist('item[]')
            ou                = request.POST.getlist('ou[]')
            product_dec       = request.POST.getlist('product_desc[]')
            unit_price        = request.POST.getlist('unit_price[]')
            extended_total    = request.POST.getlist('extended_total[]')
            
            for i in range(len(qty)):
                
                # sales   =OrderProduct(
                #     sale             = sales_id,
                #     quantity         = qty[i],
                #     item             = item[i],
                #     ou               = ou[i],
                #     production_desc  = product_dec[i],
                #     unitprice        = unit_price[i],
                #     extend           = extended_total[i]
                #     )
                # sales.save()
            #send email
                
                #get product name
                product   = Product.objects.get(id=item[i])
                

                
                context = {
                    "ITEM": product.item,
                    "DESCRIPTION": product_dec[i],
                    "QTY": qty[i],
                    "UNITPRICE": unit_price[i],
                    "EXTENDEDPRICE": extended_total[i],

                }

                totalprice =totalprice+ int(extended_total[i])
                context_list.append(context)
                template = get_template('invoice.html')


            # context = { "name": 'Hello', }
            html_string = render_to_string('invoice.html', {'context':context_list,'terms':request.POST['terms'], 'user':user, 'totalprice':totalprice})
            html = HTML(string=html_string)
            buffer = io.BytesIO()
            html.write_pdf(target=buffer)
            pdf = buffer.getvalue()

            filename = 'Invoice.pdf'
            to_emails = [request.POST['email'],]
            subject = "From CliMan"
            email = EmailMultiAlternatives(subject, "helloji", from_email="rishabhsenger7530@gmail.com", to=to_emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,"Data Submitted Successfully")


            return render(request,'form-validation.html', {'mylist':mylist,'itemid':itemid,'itemname':itemname,'user_perm':collection_perm,'sales_perm':sales_perm})
        else:
            return render(request,'form-validation.html' ,  {'mylist':mylist,'itemid':itemid,'itemname':itemname,'user_perm':collection_perm,'sales_perm':sales_perm})
    else:
        return redirect('/login')

def signup(request):
    form = Usersignupform()
    if request.method=="POST":
        form = Usersignupform(request.POST)
        
        #print(form,"formformformform")
        if form.is_valid():
            
            username = form.cleaned_data['email']
            if User.objects.filter(email=username).exists():
                messages.info(request,"Email already taken")
            else:
                form.save() 
                print("******************************")
                # instance.username = username
                # instance.save()
                messages.info(request,"Data Submitted Successfully")
        else:
            form = Usersignupform(request.POST)
    
    
    return render(request,'sign-up.html',{'form':form})


def login_req(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            print("**************")
            
               
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(username=username, password=password)
            print(username,password,"wwewew",user)
            if user is not None:
                login(request,user)
                #messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        
        form = Usersignupform()
        return render(request,'login.html', context={"form":form})



def sendSimpleEmail(request):
    

     # Rendered
    template = get_template('data-tables.html')
    context = {
        "billno": "bill_num",
        "billdate": "bill_date",
        "patientname": "patient_name",
        "totalbill": "total_bill",
        "billprocedure": "invoice_cal",

    }

    context = { "name": 'Hello', }
    html_string = render_to_string('data-tables.html', context)
    html = HTML(string=html_string)
    buffer = io.BytesIO()
    html.write_pdf(target=buffer)
    pdf = buffer.getvalue()

    filename = 'Invoice.pdf'
    s = 'rishabhsenger7530@gmail.com'
    to_emails = [s,]
    subject = "From CliMan"
    email = EmailMultiAlternatives(subject, "helloji", from_email="rishabhsenger7530@gmail.com", to=to_emails)
    email.attach(filename, pdf, "application/pdf")
    email.send(fail_silently=False)




    return redirect('/')


def myorder(request):
    if request.user.is_authenticated and  User.objects.filter(pk=request.user.id, groups__name='sales').exists():
        # cursor = connection.cursor()
        today = date.today()
        print(today,"csdsdsd")
        sql = Sales.objects.raw('''
              SELECT tp.id, tp.b_firmname, tp.b_buyer, tp.b_purchase_order, tp.email, tp.contact1, tp.b_date FROM testapp_Sales as tp 
              where  payment_due_date >= %s ''',  [today])
        collection_perm = User.objects.filter(pk=request.user.id, groups__name='collection').exists()
        sales_perm = User.objects.filter(pk=request.user.id, groups__name='sales').exists()
        return render(request,'all_order.html',{'sales':sql, 'user_perm':collection_perm,'sales_perm':sales_perm})
    else:
        return redirect('/login')


def managefollowup(request):
    if request.user.is_authenticated and  User.objects.filter(pk=request.user.id, groups__name='collection').exists():
        # cursor = connection.cursor()
        today = date.today()
        print(today,"csdsdsd")
        sql = Sales.objects.raw('''
              SELECT tp.id, tp.b_firmname, tp.b_buyer, tp.b_purchase_order, tp.email, tp.contact1, tp.b_date FROM testapp_Sales as tp 
              where  payment_due_date < %s''',  [today])

        collection_perm = User.objects.filter(pk=request.user.id, groups__name='collection').exists()
        sales_perm = User.objects.filter(pk=request.user.id, groups__name='sales').exists()
        return render(request,'manage_followup.html',{'sales':sql,'user_perm':collection_perm,'sales_perm':sales_perm})
    else:
        return redirect('/login')





def vieworder(request, pk):
    if request.user.is_authenticated :
        cursor = connection.cursor()
        today = date.today()
        
        sql = Sales.objects.raw('''
              SELECT tp.* FROM testapp_Sales as tp
              where  tp.id = %s''',  [pk])
        for i in sql:
            print(i)

        sql1 = cursor.execute('''
              SELECT op.*,p.* FROM testapp_Sales as tp
              join testapp_OrderProduct as op using(id)
              join  testapp_Product as p using(id)
              where tp.id <= %s''',  [pk])
              
        all_product = Product.objects.all()
        itemid   = []
        itemname = []
        for i in all_product:
            itemid.append(i.id)
            itemname.append(i.item)
        mylist = zip(itemid, itemname)
        collection_perm = User.objects.filter(pk=request.user.id, groups__name='collection').exists()
        sales_perm = User.objects.filter(pk=request.user.id, groups__name='sales').exists()
        return render(request,'view-sales.html',{'sales':sql,'product':sql1,'mylist':mylist,'user_perm':collection_perm,'sales_perm':sales_perm})

    else:
        return redirect('/login')


def followup(request, pk):
    if request.user.is_authenticated :
        collection_perm = User.objects.filter(pk=request.user.id, groups__name='collection').exists()
        sales_perm = User.objects.filter(pk=request.user.id, groups__name='sales').exists()
        if request.method=="POST":
            saledata=Sales.objects.get(id=pk)
            data = Followupnotes(
                sale    = saledata,
                content = request.POST['addnotes']
                )
            data.save()

        cursor = connection.cursor()
        today = date.today()
        
        sql = Sales.objects.raw('''
              SELECT tp.* FROM testapp_Sales as tp
              where  tp.id = %s''',  [pk])
        for i in sql:
            print(i)

        sql1 = cursor.execute('''
              SELECT op.*,p.* FROM testapp_Sales as tp
              join testapp_OrderProduct as op using(id)
              join  testapp_Product as p using(id)
              where tp.id <= %s''',  [pk])
              
        all_product = Product.objects.all()
        itemid   = []
        itemname = []
        for i in all_product:
            itemid.append(i.id)
            itemname.append(i.item)
        mylist = zip(itemid, itemname)
        
        #fetch notes
        followupdata = Followupnotes.objects.all()
        return render(request,'followup.html',{'sales':sql,'product':sql1,'mylist':mylist,'followupdata':followupdata,'user_perm':collection_perm,'sales_perm':sales_perm})

    else:
        return redirect('/login')

#see all users
def fetchitems(request):
    if request.method=="POST":
        id = request.POST['option']
        all_product = Product.objects.filter(id=id).values()# if request.user.has_perm('testapp.can_add_cost_price'):
        print(all_product)
        return JsonResponse({"models_to_return": list(all_product)})



def logout_view(request):
    logout(request)
    messages.info(request,"Logout Successfully")
    return redirect("/login")
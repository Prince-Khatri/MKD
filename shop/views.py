from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate,Invoice
from math import ceil
import re


# Here are the funcitons and the elements which are required for the other templates
products = Product.objects.all()

def emailChecker(email):
    # A simple regex for validating email format
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    return False

def checkEmpty(fieldName, formElement):
    
    if formElement == None or formElement == 'NaN' or formElement.strip() == '':
        thank = 0
        message = f"Error!! Kindly Enter {fieldName}."
        params = {'cat': categories, 'thank': thank, 'message': message}
        return params
    return {}  # Return empty dictionary when no errors are found

def findCategories(products):
    cat = {x.category for x in products}
    return cat

def createList(products):
    ret =[]
    l=[]
    subl=[]

    cat = findSubCategory(products)
    products = list(products)

    for cat_i in cat:
        for product in products:
            if product.sub_category == cat_i:
                subl.append(product)
            
        l.append(subl)
        n=len(subl)
        noOfSlides = n//4 + ceil( n/4 - n//4 )
        l.append(range(1,noOfSlides))
        ret.append(l)
        subl = []
        l = []
    return ret

def findSubCategory(products):
    cat =[]
    cat_i = ''
    for product in products:
        cat_i = product.sub_category
        if cat_i not in cat:
            cat.append(cat_i)
            
            
    return cat

def rangeForCat(cat):
    ran = []
    for cat_i in cat:
        n = len(cat_i)
        noOfSlides = n//4 + ceil( n/4 - n//4 )
        ran.append(range(0,noOfSlides))
    return ran

categories = findCategories(products)

# ---------main templates-------------
def index(request):

    params = createList(products)

    parameters = {'parameters':params,'cat':categories}

    return render(request,'shop/index.html',parameters)

def about(request):
    return render(request,'shop/about.html',{'cat':categories})

def search(request):
    return render(request,'shop/search.html',{'cat':categories})

def cart(request):
    return render(request,'shop/cart.html',{'cat':categories})

def product(request,prId):
    product = Product.objects.filter(id = prId)
    sameCatProducts = Product.objects.filter(sub_category = product[0].sub_category)
    n = len(sameCatProducts)
    noOfSlides = n//4 + ceil(n/4 - n//4)
    
    return render(request,'shop/product.html',{'product':product[0],'products':sameCatProducts,'range':range(1,noOfSlides),'cat':categories})

def category(request,category):
   
    cat_product = [x for x in products if x.category == category]

    return render(request,'shop/category.html',{'category':category,'cat':categories,'catProd':cat_product})

def contact(request):
    flag = 0
    message = ''
    if request.method == "POST":

        userName = request.POST.get('userName',default='')
        if not userName:
            flag = 2
            message = "Error!! Kindly Enter Name."
            return render(request,'shop/contact.html',{'cat':categories,'flag':flag,'message':message})

        userEmail = request.POST.get('userEmail',default='')
        if not userEmail:
            flag = 2
            message = "Error!! Kindly Enter Email."
            return render(request,'shop/contact.html',{'cat':categories,'flag':flag,'message':message})
        
        userPhone = request.POST.get('userPhone',default='')
        if not userPhone:
            flag = 2
            message = "Error!! Kindly Enter Phone."
            return render(request,'shop/contact.html',{'cat':categories,'flag':flag,'message':message})

        userMessage = request.POST.get('userMessage',default='')
        if not userMessage:
            flag = 2
            message = "Error!! Kindly Enter Name."
            return render(request,'shop/contact.html',{'cat':categories,'flag':flag,'message':message})
            
            
            
        
        contact = Contact(userName=userName,userEmail=userEmail,userPhone=userPhone,userMessage=userMessage)

        try:
            contact.save()
            flag = 1
            message = 'Your message has been sent successfully!'
        except Exception as e:
            flag = 2
            print('Exception',e)
            message = 'An Error occured!!!! Kindly Contact us later.'

    return render(request,'shop/contact.html',{'cat':categories,'flag':flag,'message':message})

def checkout(request):
    if request.method == "POST":
        # Cart Items
        cart = request.POST.get("cartItems", default='NaN')
        parameters = checkEmpty('Cart Items', cart)
        if parameters:  
            return render(request, 'shop/checkout.html', parameters)

        # First Name
        first_name = request.POST.get("firstName", default='NaN')
        parameters = checkEmpty('First Name', first_name)
        if parameters: 
            return render(request, 'shop/checkout.html', parameters)

        # Name = First + Last
        last_name = request.POST.get("lastName", default='')
        name = first_name + ' ' + last_name

        # Email Checking
        email = request.POST.get("custEmail", default='NaN')
        parameters = checkEmpty('Email',email)

        if parameters:
            return render(request, 'shop/checkout.html', {'cat':categories})

        # Phone
        phone = request.POST.get("custPhone", default='NaN')
        parameters = checkEmpty('Phone', phone)
        if parameters:
            return render(request, 'shop/checkout.html', parameters)

        # Address
        address = request.POST.get("address", default='NaN')
        parameters = checkEmpty('Address', address)
        if parameters:
            return render(request, 'shop/checkout.html', parameters)
        address = address + ',' + request.POST.get("address2", default='')

        # City
        city = request.POST.get("custCity", default='NaN')
        parameters = checkEmpty('City', city)
        if parameters:
            return render(request, 'shop/checkout.html', parameters)

        # Zip Code
        zipCode = request.POST.get("zipCode", default='NaN')
        parameters = checkEmpty('Zip Code', zipCode)
        if parameters:
            return render(request, 'shop/checkout.html', parameters)
        
        # State
        state = request.POST.get("custState", default='NaN')  # Correct field for state
        parameters = checkEmpty('State', state)
        if parameters:
            return render(request, 'shop/checkout.html', parameters)


        # Creating the Order object
        order = Order(cart=cart, name=name, email=email, phone=phone, address=address, city=city, state=state, zipCode=zipCode)

        try:
            # Saving the order
            order.save()
            update =  OrderUpdate(ordId = order.ordId)
            invoice = Invoice(ordId = order.ordId)
            update.setUpdate("Order Has Been Placed Successfully.")
            invoice.save()
            invoice.generateInvoicePdf()
            invoice.save()
            thank = 1
            message = 'Order Placed Successfully'
            return render(request, 'shop/checkout.html', {'cat': categories, 'thank': thank, 'message': message, 'id':order.ordId})
        except Exception as e:
            # Handle any exceptions during order saving
            thank = 0
            print(f"Exception raised while placing the order: {e}")
            message = 'Error occurred while placing the order, please try again.'
            return render(request, 'shop/checkout.html', {'cat': categories, 'thank': thank, 'message': message})


    return render(request, 'shop/checkout.html', {'cat': categories})

def tracker(request):

    if request.method == 'POST':
        ordId = request.POST.get('orderId',default = '')
        email = request.POST.get('custEmail',default = '')

        try:
            order = Order.objects.get(ordId = ordId,email = email)
            invoice = Invoice.objects.get(ordId = ordId)
            updates = OrderUpdate.objects.get(ordId = order.ordId)
            return render(request,'shop/tracker.html',{'cat':categories,'updates':updates.updates,'updateFlag':1,'invoice':invoice})


        except Exception as e:
            print(f'Exception occured:{e}')
            return render(request,'shop/tracker.html',{'cat':categories,'updateFlag':2})

    return render(request,'shop/tracker.html',{'cat':categories})
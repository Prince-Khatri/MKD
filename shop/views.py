from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact
from math import ceil

# Create your views here.
products = Product.objects.all()

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


def index(request):

    params = createList(products)

    parameters = {'parameters':params,'cat':findCategories(products)}

    return render(request,'shop/index.html',parameters)

def about(request):
    return render(request,'shop/about.html',{'cat':findCategories(products)})




def tracker(request):
    return render(request,'shop/tracker.html',{'cat':findCategories(products)})


def search(request):
    return render(request,'shop/search.html',{'cat':findCategories(products)})




def checkout(request):
    return render(request,'shop/checkout.html',{'cat':findCategories(products)})


def cart(request):
    return render(request,'shop/cart.html',{'cat':findCategories(products)})


def product(request,prId):
    product = Product.objects.filter(id = prId)
    sameCatProducts = Product.objects.filter(sub_category = product[0].sub_category)
    n = len(sameCatProducts)
    noOfSlides = n//4 + ceil(n/4 - n//4)
    print(sameCatProducts)
    return render(request,'shop/product.html',{'product':product[0],'products':sameCatProducts,'range':range(1,noOfSlides),'cat':findCategories(products)})

def category(request,category):
    print(category)
    cat_product = [x for x in products if x.category == category]

    return render(request,'shop/category.html',{'category':category,'cat':findCategories(products),'catProd':cat_product})

def contact(request):
    flag = 0
    message = ''
    if request.method == "POST":

        userName = request.POST.get('userName',default='')
        if not userName:
            flag = 2
            message = "Error!! Kindly Enter Name."
            return render(request,'shop/contact.html',{'cat':findCategories(products),'flag':flag,'message':message})

        userEmail = request.POST.get('userEmail',default='')
        if not userEmail:
            flag = 2
            message = "Error!! Kindly Enter Email."
            return render(request,'shop/contact.html',{'cat':findCategories(products),'flag':flag,'message':message})
        
        userPhone = request.POST.get('userPhone',default='')
        if not userPhone:
            flag = 2
            message = "Error!! Kindly Enter Phone."
            return render(request,'shop/contact.html',{'cat':findCategories(products),'flag':flag,'message':message})

        userMessage = request.POST.get('userMessage',default='')
        if not userMessage:
            flag = 2
            message = "Error!! Kindly Enter Name."
            return render(request,'shop/contact.html',{'cat':findCategories(products),'flag':flag,'message':message})
            
        
            
        
        contact = Contact(userName=userName,userEmail=userEmail,userPhone=userPhone,userMessage=userMessage)

        try:
            contact.save()
            flag = 1
            message = 'Your message has been sent successfully!'
        except Exception as e:
            flag = 2
            print('Exception',e)
            message = 'An Error occured!!!! Kindly Contact us later.'

    return render(request,'shop/contact.html',{'cat':findCategories(products),'flag':flag,'message':message})


    


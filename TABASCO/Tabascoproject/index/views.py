from itertools import product
from django.shortcuts import render
from .models import Category,Product

def home_page(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    context={'categories':categories,'products':products}
    return render(request , 'home.html' , context)
def category_page(request,pk):
    category= Category.objects.get(id=pk)
    products= Product.objects.filter(product_category=category)
    context={
        'category':category,
        'products':products,
    }
    return render(request,'category.html',context)
def product_page(request,pk):
    product = Product.objects.get(id=pk)
    context={
        'product':product
    }

    return render(request,'product.html',context)


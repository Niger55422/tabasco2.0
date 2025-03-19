from django.contrib.staticfiles.finders import searched_locations
from django.shortcuts import render, redirect
from .models import Category,Product,Cart
from .forms import RegForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.views import View

def home_page(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    cart_length=len(Cart.objects.filter(user_id=request.user.id))
    context={'categories':categories,'products':products,'cart':cart_length}
    return render(request , 'home.html' , context)

def category_page(request,pk):
    category= Category.objects.get(id=pk)
    cart_length=len(Cart.objects.filter(user_id=request.user.id))
    products= Product.objects.filter(product_category=category)
    context={
        'category':category,
        'products':products,
        'cart':cart_length,
    }
    return render(request,'category.html',context)
def product_page(request,pk):
    product = Product.objects.get(id=pk)
    cart_length=len(Cart.objects.filter(user_id=request.user.id))
    context={
        'product':product,
        'cart': cart_length,
    }

    return render(request,'product.html',context)
class Register(View):
    template_name= 'registration/register.html'

    def get(self,request ):
        context = {'form':RegForm}
        return render(request,self.template_name,context)
    def post(self, request):
        form=RegForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password2')
            user=User.objects.create_user(username=username,
                                          email=email,
                                          password=password).save()
            login(request, user)
            return redirect('/')
def search_product(request):
    if request.method =='POST':
        get_product= request.POST.get('search_product')
        cart_length = len(Cart.objects.filter(user_id=request.user.id))

        searched_product= Product.objects.filter(product_name__iregex=get_product)
        if search_product:
            context={'products':searched_product, 'cart':cart_length,}
            return render(request,'result.html',context)
        else:
            return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

def add_to_card(request,pk):
    if request.method =='POST':
        product = Product.objects.get(id=pk)
        if 1<= int(request.POST.get('pr_count')) <=product.product_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_count=int(request.POST.get('pr_count'))).save()
            return redirect('/')
        return redirect(f'/product/{pk}')

def delete_from_cart(request,pk):
    pr_to_del=Product.objects.get(id=pk)
    Cart.objects.filter(user_product=pr_to_del).delete()

    return redirect('cart')

def cart_page(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    total=[round(t.user_pr_count*t.user_product.product_price,2)for t in user_cart]
    context = {'cart':user_cart,'total':round(sum(total),2),'cart_l':len(user_cart)}
    return render(request,'cart.html',context)

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from taggit.models import Tag
from core.models import Product, Category, CartOrder, CartOrderProducts, ProductImages, wishlist_model, Address, ProductReview
from core.forms import ProductReviewForm
from django.db.models import Count, Avg
# Create your views here.
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers
from userauths.models import ContactUs

def index(request):
    products = Product.objects.all()
    #products = Product.objects.filter(condition1,condition2,...) <-- this here is to filter products for a specific type of product to be shown
    context = {
        "products":products
    }
    return render(request, 'core/index.html', context)

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories":categories
    }
    return render(request, 'core/category-list.html', context)

def product_list_view(request):
    products = Product.objects.all().order_by("-id")
    tags = Tag.objects.all().order_by("-id")[:6]
    category = Category.objects.all()

    context = {
        "products":products,
        "tags":tags,
        "category":category
    }

    return render(request, 'core/product-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(category = category)
    context = {
        "category":category,
        "products":products
    }
    return render(request,"core/category-product-list.html",context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()
    #products = Product.objects.filter(category=product.category).exclude(pid)
    reviews = ProductReview.objects.filter(product=product)
    review_form = ProductReviewForm()
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
        
    context = {
        "product":product,
        "p_images":p_images,
        #"products":products,
        "reviews":reviews,
        "review_form":review_form,
        "make_review":make_review
    }
    #print(reviews.review)
    return render(request,'core/product-detail.html',context)

def wip_view(request):
    return render(request, "core/wip.html")

#def product_review_view(request, pid):
#    product = Product.objects.get(pid = pid)
#    reviews = ProductReview.objects.filter(product = product)
#    context = {
#        "product" : product,
#        "reviews" : reviews
#    }
#    return render(request, '')

def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating']
    }
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews,
        }
    )

def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "core/search.html", context)

def add_to_cart(request):
    cartProduct = {}
    cartProduct[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'img':request.GET['img'],
        'pid':request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cartProduct[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cartProduct)
            request.session['cart_data_obj'] = cart_data 
    else:
        request.session['cart_data_obj'] = cartProduct
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalCartItems':len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amt = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amt += int(item['qty']) * float(item['price'])
        return render(request,"core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalCartItems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amt})
    else:
        #return render(request,"core/cart.html",{"cart_data":'', 'totalCartItems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amt})
        messages.warning(request,"your cart is empty")
        return redirect("core:index")

def delete_item_from_cart(request):
    cart_total_amt = 0
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amt += int(item['qty']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalCartItems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amt})
    return JsonResponse({"data":context, "totalCartItems":len(request.session['cart_data_obj'])})

def update_cart(request):
    cart_total_amt = 0
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amt += int(item['qty']) * float(item['price'])
    
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalCartItems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amt})
    return JsonResponse({"data":context, "totalCartItems":len(request.session['cart_data_obj'])})


def about_us(request):
    products = Product.objects.all()
    context = {
        "products":products
    }
    return render(request, "core/about_us.html", context)

def purchasing_guide(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products":products,
        "categories":categories
    }
    return render(request, "core/purchasing_guide.html", context)

def TOS(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products":products,
        "categories":categories
    }
    return render(request,"core/terms_of_service.html", context)

def privacy_policy(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products":products,
        "categories":categories
    }
    return render(request,"core/privacy_policy.html", context)

@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully.")
        return redirect("core:dashboard")
    else:
        print("Error")
        
    context = {
        "orders":orders,
        "address":address
    }
    return render(request,"core/dashboard.html", context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id =id)
    products = CartOrderProducts.objects.filter(order=order)
    context = {
        "products": products
    }
    return render(request,'core/order-detail.html', context)

@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.all()
    context = {
        "wishlists":wishlist
    }
    return render(request,"core/wishlist.html", context)

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    context = {}
    wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
    
    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
            product = product,
            user = request.user
        )
        context = {
            "bool" : True
        }
    
    return JsonResponse(context)

def remove_from_wishlist(request):
    product_id = request.GET['id']
    wishlist = wishlist_model.objects.filter(user=request.user)
    wishlist_id = wishlist_model.objects.get(id = product_id)
    delete_product = wishlist_id.delete()
    
    context = {
        "bool":True,
        "wishlists":wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('core/async/wishlist-list.html', context)
    return JsonResponse({'data':t,'wishlists':wishlist_json})


def contact(request):
    return render(request, "core/contact.html")

def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']
    contact = ContactUs.objects.create(
        full_name = full_name,
        email = email,
        phone = phone,
        subject = subject,
        message = message
    )
    data = {
        "bool": True,
        "message":"message Sent Successfully"
    }
    return JsonResponse({"data":data})
from django.http import HttpResponse
from django.shortcuts import render
from taggit.models import Tag
from core.models import Product, Category, CartOrder, CartOrderProducts, ProductImages, wishlist_model, Address, ProductReview
# Create your views here.

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

    context = {
        "products":products,
        "tags":tags,
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
    context = {
        "product":product,
        "p_images":p_images,
        #"products":products,
        "reviews":reviews
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
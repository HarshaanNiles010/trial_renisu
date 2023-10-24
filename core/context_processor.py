from core.models import Product, Category, CartOrder, CartOrderProducts, ProductImages, wishlist_model, Address, ProductReview
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        try:
            wishlist = wishlist_model.objects.filter(user=request.user)
        except:
            messages.warning(request, "You need to login before accessing your wishlist.")
            wishlist = 0
    else:
        wishlist = 0
    try:
        address = Address.objects.get(user=request.user.id)
    except Address.DoesNotExist:
        address = None
    return {
        'categories':categories,
        'address':address,
        'wishlist':wishlist,
    }
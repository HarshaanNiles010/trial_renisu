from core.models import Product, Category, CartOrder, CartOrderProducts, ProductImages, wishlist_model, Address, ProductReview



def default(request):
    categories = Category.objects.all()
    try:
        address = Address.objects.get(user=request.user.id)
    except Address.DoesNotExist:
        address = "Address not found"
    return {
        'categories':categories,
        'address':address
    }
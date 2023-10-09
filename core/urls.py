from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
     path('',views.index, name="index"),
     path("products/",views.product_list_view, name = "product-list"),
     path("category/",views.category_list_view, name = "category-list"),
     path("category/<cid>/",views.category_product_list_view, name = "category-product-list"),
     path("product/<pid>/",views.product_detail_view, name = "product-detail"),
     path("ajax-add-review/<pid>/", views.ajax_add_review, name = "ajax-add-review" ),
     path("search/", views.search_view, name="search"),
     path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
     path("cart/", views.cart_view, name="cart"),
     path("delete-from-cart/",views.delete_item_from_cart, name="delete-from-cart"),
     path("update-cart/",views.update_cart,name="update-cart"),
     # This url is only used for work in progress apps
     path('wip/',views.wip_view, name = "wip" )
]
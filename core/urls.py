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
     
     path("about_us/", views.about_us, name="about_us"),
     
     path("purchasing_guide/", views.purchasing_guide, name="purchasing_guide"),
     
     path("terms_of_service/", views.TOS, name="terms_of_service"),
     
     path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
     
     path("dashboard/", views.customer_dashboard, name="dashboard"),
     
     path("dashboard/order/<int:id>", views.order_detail, name="order-detail"),
     
     path("wishlist/", views.wishlist_view, name="wishlist"),
     
     path("add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),
     
     path("remove-from-wishlist/", views.remove_from_wishlist, name="remove-from-wishlist"),

     path("contact/", views.contact, name="contact"),
     
     path("ajax-contact-form/", views.ajax_contact_form, name="ajax-contact-form"),
     # This url is only used for work in progress apps
     path('wip/',views.wip_view, name = "wip" )
]
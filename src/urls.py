from django.urls import path
from . import views


urlpatterns = [

    #=======================USER PAGES==========================
    path("", views.index),
    path("category-products/<slug:slug>", views.category_product, name="category_products"),
    path("event-detail/<slug:slug>", views.event_detail, name="event_detail"),

    path("no-more-tickets", views.no_more_tickets, name="no_more_tickets"),

    path("cart-detail", views.cart_detail, name="cart_detail"),
    path("orders", views.user_orders, name="orders"),

    #======================CART FUNCTIONS============================
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("checkout", views.checkout, name="checkout"),
    path("show-guest", views.show_guest, name="show_guest"),
    path("guest-checkout", views.guest_checkout, name="guest_checkout"),
    
    #===========================AUTH URLS==========================
    path("sign-up", views.sign_up, name="sign_up"),
    path("sign-in", views.sign_in, name="sign_in"),
    path("logout", views.logout, name="logout"),

    #======================USER CODE URLS===========================
    path("dashboard", views.dashboard, name="dashboard"),
    path("add-event", views.add_event, name="add_event"),
    path("approuve-profile/<int:profile_id>", views.approuve_profile, name="approuve_profile"),
    path("user-profiles", views.user_profiles, name="user_profiles"),


    path("admin-index", views.admin_index, name="admin_index"),
    path("save-qr", views.save_qr, name="save_qr"),
    path("show", views.show, name="show"),

    path("hundred-qr", views.hundred_qr, name="hundred_qr"),

    #======================ADMIN LOGIN URLS=====================
    path("check-code", views.check_code, name="check_code"),

    path("ticket-checked/<int:order_id>", views.ticket_checked, name="ticket_checked"),
    path("guest-ticket-checked/<int:guest_order_id>", views.guest_ticket_checked, name="guest_ticket_checked"),

]
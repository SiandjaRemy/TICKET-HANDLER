from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import decimal, random, string
from django.contrib import messages
from .models import Profile, Event, Category, Order, Guest, GuestOrder, QrInfo, Cart, Stadium
from .forms import CodeForm, AddEventForm
import datetime
from django.utils import timezone




#======================USER PAGES=========================================
# HOME
@login_required(login_url="sign_in")
def index(request):
    events = Event.objects.filter(is_active=True)
    categories = Category.objects.filter(is_going_on=True)
    orders = Order.objects.filter(user=request.user, ticket_checked=False, date_passed=False)
    order_len = len(orders)
    cart = Cart.objects.filter(user=request.user)
    in_cart = len(cart)
    guest_orders = GuestOrder.objects.filter(user=request.user, ticket_checked=False, date_passed=False)
    time = datetime.datetime.now(timezone.utc)

    for event in events:
        name = event.title
        if event.event_date_time <= time:
            Event.objects.filter(title=name).update(is_active=False)
            
    for order in orders:
        update_event_date = order.event.id
        if order.ordered_event_date_time <= time:
            Order.objects.filter(event=update_event_date).update(date_passed=True)

    for guest_order in guest_orders:
        update_event_date = guest_order.event.id
        if guest_order.guest_order_event_date_time <= time:
            GuestOrder.objects.filter(event=update_event_date).update(date_passed=True)

    context = {
        "events":events,
        "categories":categories,
        "orders":orders,
        "order_len":order_len,
        "cart":cart,
        "in_cart":in_cart
    }
    return render(request, "list.html", context)

def date_passed(request, order_id):
    pass

#CATEGORIES
@login_required(login_url="sign_in")
def category_product(request, slug):
    category = get_object_or_404(Category, slug=slug)
    events = Event.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_going_on=True)
    orders = Order.objects.filter(user=request.user, date_passed=False, ticket_checked=False)
    order_len = len(orders)
    cart = Cart.objects.filter(user=request.user)
    in_cart = len(cart)
    
    context = {
        "category":category,
        "events":events,
        "categories":categories,
        "orders":orders,
        "order_len":order_len,
        "cart":cart,
        "in_cart":in_cart
    }

    return render(request, "list.html", context)

@login_required(login_url="sign_in")
def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    cart = Cart.objects.filter(user=request.user)
    in_cart = len(cart)
    orders = Order.objects.filter(user=request.user, date_passed=False, ticket_checked=False)
    order_len = len(orders)

    context = {
        "event":event,
        "orders":orders,
        "order_len":order_len,
        "cart":cart,
        "in_cart":in_cart,
    }

    return render(request, "detail.html", context)

def no_more_tickets(request):
    messages.info(request, "Sorry, this event is booked")
    return redirect("/")

#CART
@login_required(login_url="sign_in")
def cart_detail(request):
    events = Event.objects.filter(is_active=True)
    cart_events = Cart.objects.filter(user=request.user)
    in_cart = len(cart_events)
    orders = Order.objects.filter(user=request.user, ticket_checked=False, date_passed=False)
    order_len = len(orders)

    amount = decimal.Decimal(0)

    for c in cart_events:
        if c.event.is_active == False:
            c.delete()
            messages.info(request, f"{c.event.title} has been removed from your cart")
            return redirect("cart_detail")
            
    
    ce = [e for e in Cart.objects.all() if e.user==request.user]
    if ce:
        for e in ce:
            temp_amount = (e.quantity * e.event.ticket_price)
            amount += temp_amount
    else:
        context = {
            "orders":orders,
            "cart_events":cart_events,
            "order_len":order_len,
        }
        return render(request, "cart.html", context)

    context = {
        "events":events,
        "orders":orders,
        "order_len":order_len,
        "cart_events":cart_events,
        "in_cart":in_cart,
        "temp_amount":temp_amount,
        "amount":amount,
    }

    return render(request, "cart.html", context)

#ORDERS
@login_required(login_url="sign_in")
def user_orders(request):
    orders = Order.objects.filter(user=request.user, date_passed=False, ticket_checked=False)
    order_len = len(orders)
    cart = Cart.objects.filter(user=request.user)
    in_cart = len(cart)
    guest = Guest.objects.filter(user=request.user)
    guest_orders = GuestOrder.objects.filter(user=request.user, date_passed=False, ticket_checked=False)
    
    context = {
        "orders":orders,
        "order_len":order_len,
        "cart":cart,
        "in_cart":in_cart,
        "guest":guest,
        "guest_orders":guest_orders,
    }

    return render(request, "order.html", context)

#======================USER PAGES END=======================================

#======================CART FUNCTIONS===============================================

@login_required(login_url="sign_in")
def add_to_cart(request):
    user = request.user
    event_id = request.GET.get("ev_id")
    event = get_object_or_404(Event, id=event_id)

    item_already_in_cart = Cart.objects.filter(event=event_id, user=user)
    if item_already_in_cart:
        messages.info(request, "Sorry, 1 ticket per user")
        return redirect("/")
    else:
        Cart(user=user, event=event).save()
        return redirect("/")
    
    return redirect("/")


@login_required(login_url="sign_in")
def remove_from_cart(request, cart_id):
    if request.method == "GET":
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Event removed from cart")
    return redirect("cart_detail")

#=====================CART FUNCTIONS END===============================================

#=========================CHECKOUTS===================================================================
def checkout(request):
    cart = Cart.objects.filter(user=request.user)
    existing_orders = Order.objects.filter(user=request.user, ticket_checked=False, date_passed=False)

    profile = Profile.objects.filter(user=request.user)

    for c in cart:
        for p in profile:

            for eo in existing_orders:
                if eo.event == c.event:
                    messages.info(request, "Sorry, you cant buy two tickets for the same event")
                    return redirect("cart_detail")
            
            orders = Order(user=request.user, event=c.event, quantity=c.quantity, user_code=p.user_code, ordered_event_date_time=c.event.event_date_time)
            new_number = (c.event.available_tickets - c.quantity)
            name = c.event.title
            Event.objects.filter(title=name).update(available_tickets=new_number)

            orders.save()
        c.delete()
    return redirect("/")

def show_guest(request):
    return render(request, "guest_info.html")

def guest_checkout(request):
    cart = Cart.objects.filter(user=request.user)
    profile = Profile.objects.filter(user=request.user)

    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        id_number = request.POST["id_number"]

        existing_guest_orders = GuestOrder.objects.filter(user=request.user, ticket_checked=False, date_passed=False, id_card_number=id_number)

        for c in cart:
            for p in profile:
                for ego in existing_guest_orders:
                    if c.event == ego.event:
                        messages.info(request, "Sorry, you cant buy two tickets of the same event for this guest")
                        return redirect("cart_detail")

                guest = Guest(user=request.user, user_code=p.user, id_card_number=id_number, name=name, age=age)

                guest_order = GuestOrder(user=request.user, user_code=p.user_code, id_card_number=id_number, event=c.event, quantity=c.quantity, guest_name=name, guest_order_event_date_time=c.event.event_date_time)

                new_number = (c.event.available_tickets - c.quantity)
                event_name = c.event.title
                Event.objects.filter(title=event_name).update(available_tickets=new_number)

                guest.save()
                guest_order.save()
            c.delete()

        return redirect("/")
#======================CHECKOUTS END===================================================================

#=====================USER AUTH VIEWS========================================

def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        contact = request.POST["contact"]
        location = request.POST["location"]
        id_card_number = request.POST["id_number"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Sorry, this email already exist")
                return redirect("sign-up")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Sorry, this username already exist")
                return redirect("sign-up")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)

                user_model = User.objects.get(username=username)
                
                profile = Profile(user=user_model, id_user=user_model.id, contact=contact, location=location, id_card_number=id_card_number)
                profile.save()
                return redirect("sign_in")
        else:
            messages.info(request, "Passwords do not match")
            return redirect("sign_up")
    
    else:
        return render(request, "sign-up.html")

def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        usercode = Profile.objects.all().filter(user=user, profile_approuved=True)

        if user is not None:
            # Also check if usercode exist in qr_info and is not just jagons
            if user.is_staff:
                auth.login(request, user)
                return redirect("dashboard")
            elif usercode:
                auth.login(request, user)
                return redirect("/")
            else:
                return render (request, "no_code.html")
        else:
            messages.info(request, "invalid credentials")
            return redirect("sign_in")
    else:
        return render(request, "sign-in.html")

@login_required(login_url="sign_in")
def logout(request):
    auth.logout(request)
    return redirect("sign_in")        

#===================USER AUTH VIEWS END=========================================

#ADMIN VIEWS
#========================USER CODE VIEWS===============================================
@login_required(login_url="sign_in")
def dashboard(request):
    return render(request, "admin_page/dashboard.html")

@login_required(login_url="sign_in")
def admin_index(request):
    codes = QrInfo.objects.all()
    code_count = len(codes) #codes.count()

    context = {
        "codes":codes,
        "code_count":code_count,
    }
    
    return render(request, "admin_page/index.html", context)

@login_required(login_url="sign_in")
def save_qr(request):
    user_code = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))

    if request.method == "POST":
        code = user_code
        if QrInfo.objects.filter(code=code):
            code = user_code
        else:
            qr_info = QrInfo(code=code)
            qr_info.save()
    else:
        return render(request, "admin_page/index.html")
    return redirect("admin_index")

@login_required(login_url="sign_in")
def hundred_qr(request):
    for i in range(5):
        save_qr(request)
    return redirect("admin_index")

@login_required(login_url="sign_in")
def show(request):
    qrs = QrInfo.objects.all()
    qrs_count = qrs.count() #len(qrs)

    context = {
        "qrs": qrs,
        "qrs_count": qrs_count
    }

    return render(request, "admin_page/show.html", context)

def add_event(request):
    return render(request, "admin_page/add_event.html")

def event_form(request):
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_event")
    else:
        form = AddEventForm()
    
    return render(request, "admin_page/add_event.html",  {"form": form})
    

#======================USER CODE VIEWS END===============================================

#========================ADMIN PAGES=======================================

#Would be better if admin generated usercode directly from user account and the code is then saved in the qr_info model 
@login_required(login_url="sign_in")
def check_code(request):
    if request.method == "POST":
        user_code = request.POST["usercode"]
        profile = Profile.objects.filter(user_code=user_code)
        name = str(profile)
        orders = Order.objects.filter(user_code=user_code, ticket_checked=False, date_passed=False)
        order_len = len(orders)
        guest = Guest.objects.filter(user=request.user)
        guest_orders = GuestOrder.objects.filter(user_code=user_code, ticket_checked=False, date_passed=False)

        if profile.exists():

            context = {
                "profile":profile,
                "name":name,
                "orders":orders,
                "order_len":order_len,
                "guest":guest,
                "guest_orders":guest_orders,
            }

            return render(request, "admin_page/user_match.html", context)
        else:
            messages.info(request, "No user with this code")
            return redirect("check_code")
    else:
        return render(request, "admin_page/admin_login.html")

#=========ACTIONS===========
def ticket_checked(request, order_id):
    if request.method == "GET":
        Order.objects.filter(id=order_id).update(ticket_checked=True)
    messages.info(request, "1 ordered event was checked")
    return redirect("check_code")
    
def guest_ticket_checked(request, guest_order_id):
    if request.method == "GET":
        GuestOrder.objects.filter(id=guest_order_id).update(ticket_checked=True)
    messages.info(request, "1 ordered event was checked")
    return redirect("check_code")
    
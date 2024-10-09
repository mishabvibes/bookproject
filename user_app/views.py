from django.shortcuts import render,redirect
from book_app.models import Book, Author,LoginTable,UserRegister
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import Cart,CartItem 
from django.conf import settings
from django.urls import reverse
import stripe
# Create your views here.



def UserApp(request) :  

    books = Book.objects.all()

    paginator = Paginator(books,4)
    page_number = request.GET.get('page')

    try: 
        page = paginator.get_page(page_number)
    
    except PageNotAnInteger:
        page = paginator.page(1)

    except EmptyPage :
        page = paginator.page(paginator.num_pages)

    return render(request,'user/index.html', {'books':books,'page':page})



def UserRegistration(request) :

    login_table = LoginTable()
    user_profile = UserRegister()

    if request.method == 'POST' :

        user_profile.username = request.POST['username']
        user_profile.first_name = request.POST['first_name']
        user_profile.last_name = request.POST['last_name']
        user_profile.email = request.POST['email']
        user_profile.password = request.POST['password1']
        user_profile.password1 = request.POST['password2']


        login_table.username = request.POST['username']
        login_table.first_name = request.POST['first_name']
        login_table.last_name = request.POST['last_name']
        login_table.email = request.POST['email']
        login_table.password = request.POST['password1']
        login_table.password1 = request.POST['password2']
        login_table.type = 'user'

        if request.POST['password1'] == request.POST['password2'] :

            user_profile.save()
            login_table.save()

            messages.info(request,'Registration success')
            return redirect('login')
        else :
            messages.info(request,'Passwords not matching')
            return redirect('register')
        
    return render(request, 'user/register.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        # Check if the user exists in LoginTable
        user_details = LoginTable.objects.filter(username=username, password1=password).first()

        if user_details:
            request.session['username'] = username  # Set session username
            user_type = user_details.type  # Get the user type

            # Redirect based on user type
            if user_type == 'user':
                return redirect('userlistbook')
            elif user_type == 'admin':
                return redirect('listview')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'user/login.html')



def Logout(request):
    if request.session.get('username'):
        del request.session['username']
        messages.success(request, 'You have been logged out successfully.')
    return redirect('login')



def SearchUserBook(request) :

    query = None
    books = None
    

    if 'q' in request.GET : 

        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

    else :
        books = []

    context = {'books':books,'query':query}

    return render(request, 'user/userbooksearch.html', context)

def userDetailBook(request,book_id) :
    book = Book.objects.get(id=book_id)
    return render(request,'user/detailbook.html',{'book':book})


def add_to_card(request,book_id) :
    book = Book.objects.get(id=book_id)

    if book.quantity > 0 :  
        cart,created = Cart.objects.get_or_create(user=request.user)
        cart_item,item_created = CartItem.objects.get_or_create(cart=cart,book=book)

        if not item_created :
            cart_item.quantity += 1
            cart_item.save()

    return redirect('viewcart')

def view_cart(request) :
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_item = CartItem.objects.all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    total_items = cart_items.count()

    context = {'cart_item':cart_item, 'cart_items':cart_items, 'total_price':total_price, 'total_items':total_items}

    return render(request, 'user/cart.html', context)


def increase_quantity(request,item_id) :
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity < cart_item.book.quantity :
        cart_item.quantity += 1
        cart_item.save()
    return redirect('viewcart')


def decrease_quantity(request,item_id) :
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('viewcart')


def remove_from_cart(request,item_id) :

    try :

        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()

    except cart_item.DoesNotExist :
        pass

    return redirect('viewcart')



def create_checkout_session(request) :
        cart_items = CartItem.objects.all()

        if cart_items :
            stripe.api_key = settings.STRIPE_SECRET_KEY

            if request.method == 'POST' :
                line_items = []
                for cart_item in cart_items :
                    if cart_item.book :
                        line_item = {
                            'price_data':{
                                'currency': 'INR',
                                'unit_amount': int(cart_item.book.price * 100),
                                'product_data': {
                                    'name':cart_item.book.title
                                },
                            },
                            'quantity': cart_item.quantity
                        }
                        line_items.append(line_item)
                
                if line_items :
                    checkout_session = stripe.checkout.Session.create(
                        payment_method_types = ['card'],
                        line_items = line_items,
                        mode = 'payment',
                        success_url = request.build_absolute_uri(reverse('success')),
                        cancel_url = request.build_absolute_uri(reverse('cancel'))
                    )

                return redirect(checkout_session.url, code=303)
            


def success(request) :
    cart_items = CartItem.objects.all()

    for cart_item in cart_items :
        product = cart_item.book
        if product.quantity >= cart_item.quantity :
            product .quantity -= cart_item.quantity
            product.save()

    cart_item.delete()
    return render(request, 'user/success.html')

def cancel(request) :
    return render(request, 'user/cancel.html')

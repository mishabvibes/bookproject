from django.urls import path
from . import views

urlpatterns = [
    path('userbooklist/',views.UserApp, name='userlistbook'),
    path('',views.UserRegistration, name='register'),
    path('login/',views.LoginPage, name='login'),
    path('logout/',views.Logout, name='logout'),
    path('searchuserbook/',views.SearchUserBook, name='usersearch'),
    path('userdetailbook/<int:book_id>',views.userDetailBook, name='userdetailbook'),
    path('add-to-cart/<int:book_id>/',views.add_to_card, name='addtocart'),
    path('view-cart/',views.view_cart, name='viewcart'),
    path('increase/<int:item_id>/',views.increase_quantity, name='increase_cart'),
    path('decrease/<int:item_id>/',views.decrease_quantity, name='decrease_cart'),
    path('remove-from-cart/<int:item_id>/',views.remove_from_cart, name='remove_cart'),
    path('create-checkout-session/',views.create_checkout_session, name='create-checkout-session'),
    path('success/',views.success, name='success'),
    path('cancel/',views.cancel, name='cancel')
]
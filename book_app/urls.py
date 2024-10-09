from django.urls import path
from . import views

urlpatterns = [
    path('createbook',views.createBook, name='createbook'),
    path('searchbook/<int:book_id>',views.view_specific,name='detail'),
    path('updatebook/<int:book_id>',views.updatebook,name='update'),
    path('deletebook/<int:book_id>',views.deletebook,name='delete'),
    path('authorform/',views.createAuthor,name='authorinfo'),
    path('adminpanel/',views.AdminPanal),
    path('home/',views.ListView, name='listview'),
    path('searchbook/',views.SearchBook, name='search'),

]
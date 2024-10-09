from django.shortcuts import render,redirect
from .models import Book,UserRegister, LoginTable
from .forms import AuthorForm,BookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User




def view_specific(request,book_id) :
    book = Book.objects.get(id=book_id)
    return render(request,'admin/viewspecific.html',{'book':book})




def updatebook(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listview')
    else:
        form = BookForm(instance=book)

    return render(request, 'admin/updatebook.html', {'form': form})



def deletebook(request,book_id) :

    book = Book.objects.get(id=book_id)

    if request.method == 'POST' :
        
        book.delete()

        return redirect('home/')
    
    return render(request,'admin/deletebook.html',{'book':book})


def createBook(request) :

    books = Book.objects.all()

    if request.method == 'POST' :

        form = BookForm(request.POST,files=request.FILES)

        if form.is_valid :
            form.save()


    else :
        form = BookForm()

    return render(request,'admin/home.html',{'form':form, 'books':books})


def createAuthor(request) :

    if request.method == 'POST' :

        form = AuthorForm(request.POST)

        if form.is_valid :
            form.save()
            return redirect('/createbook')

    else :

        form = AuthorForm()

    return render(request,'admin/author.html',{'form':form})


def AdminPanal(request) :
    return render(request, 'admin/base.html')



def ListView(request) :
    books = Book.objects.all()

    paginator = Paginator(books,4)
    page_number = request.GET.get('page')

    try: 
        page = paginator.get_page(page_number)
    
    except PageNotAnInteger:
        page = paginator.page(1)

    except EmptyPage :
        page = paginator.page(paginator.num_pages)


    return render(request, 'admin/listview.html', {'books':books,'page':page})


def SearchBook(request) :

    query = None
    books = None

    if 'q' in request.GET : 

        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

    else :
        books = []

    context = {'books':books,'query':query}

    return render(request, 'admin/search.html', context)
        

# def LoginPage(request) :

#     if request.method == 'POST' :
#         username = request.POST['username']
#         password = request.POST['password1']
#         user = LoginTable.objects.filter(username=username, password1=password,type='user').exists() 

#         try :

#             if user is not None :

#                 user_details = LoginTable.objects.get(username=username, password1=password)
#                 user_name = user_details.username
#                 type = user_details.type

#                 if type == 'user' :
#                     request.session['username'] = user_name
#                     return redirect('userlistbook')
#                 elif type == 'admin' :
#                     request.session['username'] = user_name
#                     return redirect('listview')
#             else :
#                 messages.error(request, 'Invalid username or password')
#         except :
#             messages.error(request, 'Invalid role')


#     return render(request, 'user/login.html')


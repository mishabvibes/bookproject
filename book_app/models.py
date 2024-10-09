from django.db import models

# Create your models here.

class Author(models.Model) :

    name = models.CharField(max_length=50, null=True)

    def __str__(self) :
        return '{}'.format(self.name)

class Book(models.Model) :

    title = models.CharField(max_length=50,null=True)
    price = models.IntegerField(null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='book_media')

    def __str__(self) :
        return '{}'.format(self.title)
    

class UserRegister(models.Model) :

    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password1 = models.CharField(max_length=200)

    def __str__(self) :
        return '{}'.format(self.username)
    

class LoginTable(models.Model) :

    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password1 = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self) :
        return '{}'.format(self.username)
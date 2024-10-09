from django.contrib import admin
from .models import Book,Author,UserRegister,LoginTable
# from django.contrib.admin.sites import AlreadyRegistered
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
# try:
admin.site.register(UserRegister)
# except AlreadyRegistered:
#     pass
admin.site.register(LoginTable)
from django import forms
from .models import Book,Author


class AuthorForm(forms.ModelForm) :

    class Meta :

        model = Author
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Book title'}),
        }


class BookForm(forms.ModelForm) :

    class Meta :

        model = Book
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Book title'}),
            'author': forms.Select(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Book price'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Book quantity'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'type':'file', 'id': 'authorName'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding a default placeholder option for the author field
        self.fields['author'].empty_label = "Select Author"

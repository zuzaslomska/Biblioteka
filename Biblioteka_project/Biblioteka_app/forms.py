from django import forms
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm
from .models import Book, IndustryIdentifiers, ImageLinks
import datetime


now = datetime.datetime.now()

class ImageLinksForm(forms.ModelForm):
    class Meta:
        model = ImageLinks
        fields = '__all__'
        widgets = {'small_thumbnail': forms.URLInput(),
                   'thumbnail': forms.URLInput(),
                   'small': forms.URLInput(),
                   'medium': forms.URLInput(),
                   'large': forms.URLInput(),
                   'extraLarge': forms.URLInput(),
                   }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {'image_links': forms.HiddenInput(),
                   'published_date': forms.SelectDateWidget(years=range(1850,now.year+1)),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_links'].required = False


class IndustryIdentifiersForm(forms.ModelForm):
    class Meta:
        model = IndustryIdentifiers
        fields = '__all__'
        widgets = {'book': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].required = False

class BookMultiForm(MultiModelForm):
    form_classes = {
        'image_links': ImageLinksForm,
        'book': BookForm,
        'id': IndustryIdentifiersForm,
    }

class SearchBookForm(forms.ModelForm):
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=range(1850,now.year+1)))
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=range(1850, now.year + 1)))
    class Meta:
        model = Book
        fields = ['title','author','language']



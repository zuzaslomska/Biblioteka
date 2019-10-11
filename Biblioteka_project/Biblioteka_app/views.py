from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Book, IndustryIdentifiers, ImageLinks
from django.views.generic import (FormView,CreateView,ListView,UpdateView,TemplateView,DeleteView)
from .forms import BookMultiForm


class ListOfBooks(ListView):
    template_name = 'list_of_books.html'
    model = Book


class SearchResultsView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query)
        )
        return object_list


class AddBookView(CreateView):
    form_class = BookMultiForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('list_of_books')

    def form_valid(self, form):
        image_links = form['image_links'].save()
        book = form['book'].save()
        book.image_links = image_links
        book.save()
        industryidentifiers = form['id'].save()
        industryidentifiers.book = book
        industryidentifiers.save()
        return super().form_valid(form)



    # def get_form_kwargs(self):
    #     kwargs = super(AddBookView, self).get_form_kwargs()
    #     kwargs.update(instance={
    #         'image_links': self.object,
    #         'book': self.object,
    #         'id': self.object
    #     })
    #     return kwargs

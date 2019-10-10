from django.shortcuts import render
from .models import Book, IndustryIdentifiers, ImageLinks
from django.views.generic import (FormView,CreateView,ListView,UpdateView,TemplateView,DeleteView)


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
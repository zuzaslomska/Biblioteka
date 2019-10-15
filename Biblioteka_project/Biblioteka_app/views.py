from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Book, IndustryIdentifiers, ImageLinks
from django.views.generic import (FormView,CreateView,ListView,UpdateView,TemplateView,DeleteView)
from .forms import BookMultiForm, SearchBookForm


class ListOfBooks(ListView):
    template_name = 'list_of_books.html'
    form_class = SearchBookForm

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['form'] = SearchBookForm()
        return context

    def get_queryset(self):
        queryset = Book.objects.all()
        field = self.request.GET.get
        print(field)
        title = field('title','')
        author = field('author','')
        language = field('language','')
        date_from = field('date_from_year','') + '-' + field('date_from_month','') + '-' + field('date_from_day','')
        date_to = field('date_to_year','') + '-' + field('date_to_month','') + '-' + field('date_to_day','')


        if title is not '' or author is not '' or language is not '' or len(date_from) is not 2 or len(date_to) is not 2 :
            book = Book.objects.filter(
                Q(title__icontains=title) |
                Q(author__icontains=author) |
                Q(language__icontains=language) |
                Q(published_date__range=[date_from,date_to])
            )
            queryset = book
            return queryset

        return queryset


# class SearchResultsView(ListView):
#     model = Book
#     template_name = 'search_results.html'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = Book.objects.filter(
#             Q(title__icontains=query)
#         )
#         return object_list


class AddBookView(CreateView):
    form_class = BookMultiForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('add_book')

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

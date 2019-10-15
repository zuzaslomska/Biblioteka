from django.db.models import Q
from django.urls import reverse_lazy
from .models import Book, IndustryIdentifiers, ImageLinks
from django.views.generic import (CreateView, ListView, TemplateView)
from .forms import BookMultiForm, SearchBookForm, ImportBookForm, BookFilter
from .services import get_books, camel_case_split
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters


class ListOfBooksView(ListView):
    template_name = 'list_of_books.html'
    form_class = SearchBookForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = SearchBookForm()
        return context

    def get_queryset(self):
        queryset = Book.objects.all()
        field = self.request.GET.get
        print(field)
        title = field('title', '')
        authors = field('authors', '')
        language = field('language', '')
        date_from = field('date_from_year', '') + '-' + field('date_from_month', '') + '-' + field('date_from_day', '')
        date_to = field('date_to_year', '') + '-' + field('date_to_month', '') + '-' + field('date_to_day', '')


        if title is not '' or authors is not '' or language is not '' or len(date_from) is not 2 or len(date_to) is not 2:
            book = Book.objects.filter(
                Q(title__icontains=title) |
                Q(authors__icontains=authors) |
                Q(language__icontains=language) |
                Q(published_date__range=[date_from, date_to])
            )
            queryset = book
            return queryset

        return queryset


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


class BooksPageView(TemplateView):
    template_name = 'import_books.html'
    form_class = ImportBookForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = ImportBookForm()
        return context

    def get(self, request, *args, **kwargs):
        auth_key = 'AIzaSyBGuto538TGlzaFFXRpeCOBWADhG5mX4uw'
        query = request.GET.get('query')

        if query is not None:
            x = get_books(query, auth_key)
            for i in range(len(x)):
                book = x[i]['volumeInfo', '']
                first_loop = True
                for k, v in book.get('imageLinks', {}).items():
                    k = camel_case_split(k)
                    if first_loop:
                        if k is not None:
                            image = ImageLinks.objects.create(**{k: v})
                            first_loop = False
                            continue
                    setattr(image, k, v)
                    image.save()
                    if k == 'imageLinks':
                        for x, y in k.items():
                            if first_loop:
                                image = ImageLinks.objects.create(**{k: v})
                                first_loop = False
                                continue
                            setattr(image, x, y)
                            image.save()

                if 3 < len(book.get('publishedDate', '')) < 10:
                    published_date = book.get('publishedDate') + '-' + '01' + '-' + '01'
                else:
                        published_date = book.get('publishedDate', '')

                import_book = Book.objects.create(
                                    title=book.get('title', ''),
                                    published_date=published_date,
                                    page_count=book.get('page_count'),
                                    image_links=image,
                                    language=book.get('language', ''),
                                    authors=book.get('authors', '')
                )

                for i in range(len(book.get('industryIdentifiers', ''))):
                    loop = 0
                    check = 1
                    for k, v in book.get('industryIdentifiers', {})[i].items():

                        k = camel_case_split(k)
                        if loop == check:
                            setattr(id, k, v)
                            id.save()
                            check += 1
                            continue
                        id = IndustryIdentifiers.objects.create(**{k: v}, book=import_book)
                        loop += 1
        return super().get(request)


class ListOfBooksRestView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
    queryset = Book.objects.all()



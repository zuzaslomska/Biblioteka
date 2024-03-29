"""Biblioteka_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from Biblioteka_app.views import ListOfBooksView, AddBookView, BooksPageView, ListOfBooksRestView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('home/', ListOfBooksView.as_view(), name='list_of_books'),
    path('books/page/', BooksPageView.as_view(), name='books_page'),
    path('add/book/', AddBookView.as_view(), name='add_book'),
    path('list/book/', ListOfBooksRestView.as_view(), name='list_of_books_rest'),
]

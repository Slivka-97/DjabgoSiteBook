from django.http import HttpResponse
from django.shortcuts import render

from book.form import *
from book.models import Book as ClassBook, Category, Sale

main_menu = [{"title": "Главное", "url_name": "main"},
             {"title": "Все книги", "url_name": "books"},
             {"title": "Книги по жанрам", "url_name": "category"},
             {"title": "О сайте", "url_name": "about"},
             {"title": "Войти", "url_name": "login"},
             {"title": "Регистрация", "url_name": "registration"}, ]


def main(request):
    context = {"main_menu": main_menu,
               "title": "Все книги"}
    return render(request, "book/mainPage.html", context=context)


def books(request):
    if len(request.GET) == 0:
        books = ClassBook.objects.all()
    else:
        cat = request.GET.get('cat')
        books = ClassBook.objects.filter(category=cat)

    context = {"books": books,
               "title": "Главная страница"}
    return render(request, "book/allBook.html", context=context)


def category(request):
    cat = Category.objects.all()
    return render(request, "book/books_category.html", {"category": cat, "title": "Жанры"})


def about(request):
    return render(request, "book/about.html", {"title": "О сайте"})


def login(request):
    return HttpResponse('login')


def registration(request):
    return HttpResponse('registration')


def post(request, post_name):
    book = ClassBook.objects.filter(title=post_name)
    return render(request, "book/post.html", {"book": book})


def create_book_sale(book):
    try:
        s = Sale(book=book, user='Ivan')
        s.save()
    except:
        raise AttributeError("не правельные параметры")


def sale(request, book_name):
    book = ClassBook.objects.get(title=book_name)
    if book.number_book == 0:
        return HttpResponse('К сожелению на данный момент данной книги нет на складе')
    else:
        # Надо организовать проверку на авторизованность юзера
        book.number_book -= 1
        book.save()
        create_book_sale(book)
        return HttpResponse('Книга выдана')

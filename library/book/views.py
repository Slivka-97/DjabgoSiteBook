from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from book.form import *
from book.models import Book as ClassBook, Category, Sale

main_menu = [{"title": "Главное", "url_name": "main"},
             {"title": "Все книги", "url_name": "books"},
             {"title": "Книги по жанрам", "url_name": "category"},
             {"title": "О сайте", "url_name": "about"}]


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


def loginForm(request):
    if request.method == "POST":
        form = FormLogin(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('main')

    form = FormLogin()
    return render(request, "book/login.html", {'form': form, 'title': "Авторизация"})


def registration(request):
    if request.method == "POST":
        form = FormRegest(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = FormRegest()
    return render(request, "book/register.html", {'form': form, 'title': "Регистрация"})


def post(request, post_name):
    book = ClassBook.objects.filter(title=post_name)
    return render(request, "book/post.html", {"book": book})


def create_book_sale(book, user):
    try:
        s = Sale(book=book, user=user)
        s.save()
    except:
        raise AttributeError("не правельные параметры")


def sale(request, book_name):
    book = ClassBook.objects.get(title=book_name)
    if book.number_book == 0:
        return HttpResponse('К сожелению на данный момент данной книги нет на складе')
    else:
        if request.user.is_authenticated:
            count_book = Sale.objects.filter(user=request.user.username, book=book)
            if len(count_book) == 0:
                book.number_book -= 1
                book.save()
                create_book_sale(book, request.user.username)
                return render(request, "book/good_sale.html", {"msg": "Книга выдана"})
            else:
                return render(request, "book/good_sale.html", {"msg": "У вас уже есть данная книга, выберите другую"})
        else:
            return redirect('login')


def logOut_user(request):
    logout(request)
    return redirect('main')

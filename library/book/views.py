from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page

from book.form import *
from book.models import Book as ClassBook, Category, Sale

main_menu = [{"title": "Главное", "url_name": "main"},
             {"title": "Все книги", "url_name": "books"},
             {"title": "Книги по жанрам", "url_name": "category"},
             {"title": "О сайте", "url_name": "about"}]


@cache_page(60)
def main(request):
    context = {"main_menu": main_menu,
               "title": "Все книги"}
    return render(request, "book/mainPage.html", context=context)


@cache_page(60)
def books(request):
    """Показываем список всех книг в том случае если нет дополнительного параметра в GET запросе.
    Иначе показываем книги только по указанной категории"""
    if len(request.GET) == 0:
        books = ClassBook.objects.all().select_related('category')
    else:
        cat = request.GET.get('cat')
        books = ClassBook.objects.filter(category=cat)

    context = {"books": books,
               "title": "Главная страница"}
    return render(request, "book/allBook.html", context=context)


def category(request):
    """Показывваем все категории"""
    cat = Category.objects.all()
    return render(request, "book/books_category.html", {"category": cat, "title": "Жанры"})


def about(request):
    """Небольшая информация о сайте"""
    return render(request, "book/about.html", {"title": "О сайте"})


def loginForm(request):
    """Форма для авторизации на сайте"""
    if request.method == "POST":
        form = FormLogin(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('main')

    form = FormLogin()
    return render(request, "book/login.html", {'form': form, 'title': "Авторизация"})


def registration(request):
    """Форма для регистрации на сайте"""
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
    """Показываем всю информацию по выбранной книги"""
    book = ClassBook.objects.get(title=post_name)
    return render(request, "book/post.html", {"book": book})


def create_book_sale(book, user):
    """Вспомогательный метод для записи информации в базу данных"""
    try:
        s = Sale(book=book, user=user)
        s.save()
    except:
        raise AttributeError("не правельные параметры")


def sale(request, book_name):
    """Функция выдает книгу если все условия соблюдены.
    1: Выбранная книга есть на складе.
    2: Пользователь авторизован на сайте.
    3: Если данная книга уже есть у данного пользователя , тогда книга не выдаеться"""
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
    """Выход из учетной записи"""
    logout(request)
    return redirect('main')

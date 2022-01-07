from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.CharField(max_length=255, verbose_name="Автор")
    description = models.TextField(blank=False, verbose_name="Описание")
    year_book = models.IntegerField(verbose_name="Год")
    number_book = models.IntegerField(verbose_name="Количество")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    def get_absolute_url(self):
        return reverse("post", kwargs={'post_name': self.title})

    def get_sale(self):
        return reverse('sale', kwargs={'book_name': self.title})

    class Meta:
        verbose_name = "Книги"
        verbose_name_plural = "Книги"


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Категория")

    def get_name(self):
        return self.title

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"


class Sale(models.Model):
    book = models.ForeignKey("Book", on_delete=models.PROTECT, verbose_name="Книга")
    user = models.CharField(max_length=255, verbose_name="Пользователь")
    data_sale = models.DateTimeField(auto_now_add=True, verbose_name="Дата аренды")

    class Meta:
        verbose_name = "Аренда книг"
        verbose_name_plural = "Аренда"

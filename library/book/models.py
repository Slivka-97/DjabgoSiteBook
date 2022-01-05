from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    year_book = models.IntegerField()
    number_book = models.IntegerField()
    photo = models.ImageField(upload_to="photos")
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("post", kwargs={'post_name': self.title})

    def get_sale(self):
        return reverse('sale', kwargs={'book_name': self.title})


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def get_name(self):
        return self.title


class Sale(models.Model):
    book = models.ForeignKey("Book", on_delete=models.PROTECT)
    user = models.CharField(max_length=255)
    data_sale = models.DateTimeField(auto_now_add=True)



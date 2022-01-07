from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'description', 'year_book', 'number_book', 'photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'author')


admin.site.register(Book, BookAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'data_sale')
    list_display_links = ('id', 'book')
    search_fields = ('book',)


admin.site.register(Sale, SaleAdmin)

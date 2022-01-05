from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', main, name="main"),
    path('books/', books, name='books'),
    path('post/<str:post_name>/', post, name="post"),
    path('category/', category, name='category'),
    path('about/', about, name='about'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('sale/<str:book_name>', sale, name='sale'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, docoment_root=settings.MEDIA_ROOT)

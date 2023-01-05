from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('books',views.books),
    path('addBook',views.addBook),
    path('add_books_reviews',views.addprocess),
    path('books/<int:new_book_id>',views.view),
    path('addReview',views.addReview),
    path('del_review',views.delete),
    path('users/<int:userID>',views.userview)
]
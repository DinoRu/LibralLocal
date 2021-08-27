from django.urls import path
from . import views

app_name = 'Catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'), 
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllBookUsersBorrowed.as_view(), name='all-borrowed'),
    path('books/<uuid:pk>/renew/', views.renew_book_librairian, name='renew-book-librarian'),
]
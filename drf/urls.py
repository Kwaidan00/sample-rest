from django.urls import path

from drf.views import BookDetail, BookList, AuthorList, AuthorDetail, \
    PersonalLibraryDetail, PersonalLibraryBooksList, PersonalLibraryBookDetail

app_name = 'drf'

urlpatterns = [
    path('books/', BookList.as_view(), name='books-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('authors/', AuthorList.as_view(), name='authors-list'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('user/<int:user_pk>/', PersonalLibraryDetail.as_view(), name='library-detail'),
    path('user/<int:user_pk>/books/', PersonalLibraryBooksList.as_view(),
         name='library-detail-books-list'),
    path('user/<int:user_pk>/books/<int:pk>/', PersonalLibraryBookDetail.as_view(),
         name='library-detail-book-detail'),
]

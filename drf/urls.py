from django.urls import path

from drf.views import BookDetail, BookList, AuthorList, AuthorDetail, \
    PersonalLibraryDetail

app_name = 'drf'

urlpatterns = [
    path('books/', BookList.as_view()),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('authors/', AuthorList.as_view()),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('personal-libraries/<int:pk>/', PersonalLibraryDetail.as_view(), name='library-detail'),
]

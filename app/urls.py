from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('courses/', courses, name='courses'),
    path('category_courses/<str:name>/', category_courses, name='category_courses'),
    path('tag_courses/<str:name>/', tag_courses, name='tag_courses'),
    path('toggle-like/<int:item_id>/', toggle_like, name='toggle_like'),
    path('toggle-dislike/<int:item_id>/', toggle_dislike, name='toggle_dislike'),
    path('search/', search, name='search'),
    path('contact/', CreateContactView.as_view(), name='contact'),
    path('course/<int:id>/', course_detail, name="course_detail"),
    path('course/<int:id>/<int:pk>/', lesson_detail, name="lesson_detail"),
]

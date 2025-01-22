from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import CreateContactForm, CommentForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.db.models import Q

def home(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'home.html', context)

def courses(request):
    courses = Course.objects.all()

    context = {
        'courses': courses
    }
    return render(request, 'courses.html', context)

def category_courses(request, name):
    courses = Course.objects.filter(category__name=name)

    context = {
        'courses': courses
    }
    return render(request, 'courses.html', context)

def tag_courses(request, name):
    courses = Course.objects.filter(tag__name=name)

    context = {
        'courses': courses,
    }
    return render(request, 'courses.html', context)

class CreateContactView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = CreateContactForm
    template_name = 'contact.html'
    success_url = '/'
    success_message = 'Created'


def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    tags = Tag.objects.filter(courses__id=id)
    lesson = Lesson.objects.first()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.course = course
            comment.save()
            return redirect('course_detail', id=course.id)

    else:
        form = CommentForm()

    comments = Comment.objects.filter(course=course).order_by('-created_at')

    context = {
        'course': course,
        'comments': comments,
        'tags': tags,
        'form': form,
        'lesson': lesson,
    }
    return render(request, 'course_detail.html', context)

def lesson_detail(request, id, pk):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lesson, pk=pk)
    tags = Tag.objects.filter(courses__id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.course = course
            comment.save()
            return redirect('course_detail', id=course.id)

    else:
        form = CommentForm()

    comments = Comment.objects.filter(course=course).order_by('-created_at')

    context = {
        'course': course,
        'comments': comments,
        'tags': tags,
        'form': form,
        'lesson': lesson,
    }
    return render(request, 'lesson_detail.html', context)


def toggle_like(request, item_id):
    item = get_object_or_404(Course, id=item_id)

    item.is_liked = True
    item.save()

    return redirect('courses')

def toggle_dislike(request, item_id):
    item = get_object_or_404(Course, id=item_id)

    item.is_liked = False
    item.save()

    return redirect('courses')

def search(request):
    query = request.GET.get('q', '')
    courses = []
    if query:
        courses = Course.objects.filter(
            Q(name__icontains=query) | Q(about__icontains=query)
        )
    return render(request, 'search.html', {'query': query, 'courses': courses})

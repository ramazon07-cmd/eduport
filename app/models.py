from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import datetime
from moviepy import VideoFileClip


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='courses/')
    author = models.ForeignKey('app.CustomUser', on_delete=models.CASCADE)
    paragraph1 = models.TextField()
    paragraph2 = models.TextField()
    paragraph3 = models.TextField()
    paragraph4 = models.TextField()
    lectures = models.ManyToManyField('Lecture')
    is_liked = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='courses_tags', null=True, blank=True)

    @property
    def total_video_duration(self):
        total_duration = 0
        for lecture in self.lectures.all():
            for lesson in lecture.lessons.all():
                try:
                    video_path = lesson.video.path
                    video = VideoFileClip(video_path)
                    total_duration += video.duration
                except Exception as e:
                    print(f"Error processing video for lesson {lesson.name}: {e}")

        total_seconds = int(total_duration)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        parts = []
        if hours > 0:
            parts.append(f"{hours} hours")
        if minutes > 0:
            parts.append(f"{minutes} minutes")
        if seconds > 0:
            parts.append(f"{seconds} seconds")

        return " ".join(parts)

    def __str__(self):
        return self.name


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey('app.CustomUser', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comments'


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='categories/')
    courses = models.ManyToManyField(Course, related_name='categories', blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course, related_name='tags')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to='lessons/')

    @property
    def video_duration(self):
        video_path = self.video.path
        video = VideoFileClip(video_path)
        return video.duration

    def __str__(self):
        return self.name

class Lecture(models.Model):
    name = models.CharField(max_length=255)
    lessons = models.ManyToManyField('Lesson')

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

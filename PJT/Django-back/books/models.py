from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_books')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pub_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=20)
    cover_image = models.URLField()
    aladin_link = models.URLField()
    publisher = models.CharField(max_length=200)
    customer_review_rank = models.PositiveIntegerField()

class Thread(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    read_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thread_cover = models.ImageField(upload_to='thread/', null=True, blank=True) 
    like_users = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name='liked_threads',
    blank=True
)   
    summary = models.TextField(null=True, blank=True)  # GPT 감성 분석 결과 저장용

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,related_name='comments')
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
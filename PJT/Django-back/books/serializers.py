from rest_framework import serializers
from .models import Book, Thread, Category
from .models import Comment

class BookListSerializer(serializers.ModelSerializer):
    favorite_count = serializers.IntegerField()  #  찜한 유저 수
    favorited = serializers.SerializerMethodField(read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'category', 'favorite_count', 'favorited']
        read_only_fields = ['favorited_by', 'favorited']  #  직접 수정 못 하게 막기
    
    def get_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.favorited_by.filter(id=user.id).exists()

class BookSerializer(serializers.ModelSerializer):
    favorite_count = serializers.IntegerField()  #  찜한 유저 수
    favorited = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['favorited_by', 'favorited', 'favorite_count']  #  직접 수정 못 하게 막기
    
    def get_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.favorited_by.filter(id=user.id).exists()

class ThreadSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()  #  좋아요 수 필드
    user = serializers.CharField(source='user.username', read_only=True)  #  id 대신 username 반환
    class Meta:
        model = Thread
        fields = "__all__"
        read_only_fields = ['user', 'book', 'thread_cover', 'like_users']
    def get_like_count(self, obj):
        return obj.like_users.count() #좋아요 수 계산

class ThreadListSerializer(serializers.ModelSerializer): 
    # 필요한 데이터, user => username / thread like_count, 
    like_count = serializers.IntegerField()
    liked = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'user', 'title', 'thread_cover', 'like_count', 'liked']
        read_only_fields = ['like_count', 'liked', 'user']
    
    def get_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.like_users.filter(id=user.id).exists()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)  #  id 대신 username 반환
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'thread')

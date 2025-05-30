from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from books.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False, allow_null=True)
    interested_categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )

    def get_cleaned_data(self):
        data =  super().get_cleaned_data()
        data['age'] = self.validated_data.get('age', '')
        return data

    def save(self, request):
        user = super().save(request)
        categories = self.validated_data.get('interested_categories')
        if categories:
            user.interested_categories.set(categories)
        user.age = self.validated_data.get('age', '')
        user.save()
        return user

class CustomUserDetailsSerializer(UserDetailsSerializer):
    interested_categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    age = serializers.IntegerField(required=False, allow_null=True)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + ('age', 'interested_categories',)

    def update(self, instance, validated_data):
        # ManyToMany: 관심 분야 먼저 처리
        categories = validated_data.pop('interested_categories', None)
        if categories is not None:
            instance.interested_categories.set(categories)

        # 단일 필드: age 등
        instance.age = validated_data.get('age', instance.age)

        # 나머지 기본 필드 처리
        return super().update(instance, validated_data)
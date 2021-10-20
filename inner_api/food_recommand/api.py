from django.db.models.fields import CharField, IntegerField
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        # 모델 설정
        model = Food
        # 필드 설정
        fields = ['name', 'youtube_url']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'email', 'picked_food_list', 'like_food_list', 'dislike_food_list']

class ResultSerializer(serializers.Serializer):
    pickFood = FoodSerializer(many=True)

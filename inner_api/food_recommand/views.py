from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.decorators import api_view, action, renderer_classes

from rest_framework import status, viewsets, permissions, renderers
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from food_recommand.models import Food, SelectedFood, Member
from food_recommand.api import FoodSerializer, MemberSerializer
from django.http import HttpResponse, JsonResponse
import json

import random
import urllib

def food_recommand(email, a1, a2, a3):
    try:
        member = Member.objects.filter(email=email)
    except Member.DoesNotExist:
        return None
    ret = []
    size = Food.objects.all().count()
    ret += Food.objects.filter(id = random.randrange(1, size))
    ret += Food.objects.filter(id = random.randrange(1, size))
    ret += Food.objects.filter(id = random.randrange(1, size))
    return urllib.parse.quote(list(ret))
    
class pick_foodViewSet(viewsets.ModelViewSet):
    
    serializer_class = FoodSerializer
    renderer_classes = [renderers.JSONRenderer]
    
    def get_queryset(self):
        email = self.request.GET.get('email', None)
        a1 = self.request.GET.get('answer1', None)
        a2 = self.request.GET.get('answer2', None)
        a3 = self.request.GET.get('answer3', None)
        return food_recommand(email, a1, a2, a3)

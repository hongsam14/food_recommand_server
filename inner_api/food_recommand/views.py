from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, renderer_classes
from rest_framework import status, viewsets, permissions, renderers
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from food_recommand.models import Food, SelectedFood, Member, LikeFood, DislikeFood
from food_recommand.api import FoodSerializer, ResultSerializer
import json
import random
import pandas as pd
import numpy as np

def add_by_answer(food_table:list, a1:str, a2:str, a3:str):
    a1_list = a1.split(',')
    a2_list = a2.split(',')
    a3_list = a3.split(',')
    for i in food_table:
        for j in a1_list:
            if j in i[0][1]:
                i[1] += 1
        for k in a2_list:
            if k in i[0][1]:
                i[1] += 1
        for l in a3_list:
            if l in i[0][1]:
                i[1] += 1
    food_table.sort(key=lambda x: -x[1])
    return food_table[:4]

def pick_random(query, count:int):
    ret = []
    pool = list(range(1, query.objects.all().count()))
    for _ in range(count):
        pick = random.choice(pool)
        ret += query.objects.filter(food_id = pick)
        pool.remove(pick)
    return ret

def food_recommand(id, a1, a2, a3):
    try:
        member = Member.objects.filter(member_id=id)
    except Member.DoesNotExist:
        return None
    #init
    _info = np.array(Food.objects.all().values_list('tag'))
    av_card = np.zeros((Member.objects.all().count(), Food.objects.all().count()), int)
    _liked = np.array(LikeFood.objects.all().values_list('member_id', 'food_id'), int)
    _disliked = np.array(DislikeFood.objects.all().values_list('member_id', 'food_id'), int)
    _selected = np.array(SelectedFood.objects.all().values_list('member_id', 'food_id'), int)
    print(_selected)
    #좋아하는 음식 +
    for i in _liked:
        av_card[i[0] - 1, i[1] - 1] += 1
    #싫어하는 음식 -
    for i in _disliked:
        av_card[i[0] - 1, i[1] - 1] -= 1
    #먹었던 음식 +
    for i in _selected:
        av_card[i[0] - 1, i[1] - 1] += 1
    print(av_card)
    #임시
    food_table = [[i, 0] for i in Food.objects.all().values_list('food_id', 'tag')]
    ret = []
    for i in add_by_answer(food_table, a1, a2, a3):
        ret += Food.objects.filter(food_id=i[0][0])
    return {"pickFood":ret}
    
@csrf_exempt
@api_view(['GET'])
def pickFood(request):
    if request.method == 'GET':
        email = request.GET.get('id', None)
        a1 = request.GET.get('answer1', None)
        a2 = request.GET.get('answer2', None)
        a3 = request.GET.get('answer3', None)
        serializer = ResultSerializer(food_recommand(email, a1, a2, a3))
        return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False})

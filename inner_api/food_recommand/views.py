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
from sklearn.metrics.pairwise import cosine_similarity

def pick_random(query, count:int):
    ret = []
    pool = list(range(1, query.objects.all().count()))
    for _ in range(count):
        pick = random.choice(pool)
        ret += query.objects.filter(food_id = pick)
        pool.remove(pick)
    return ret

def add_by_answer(food_table, a1:str, a2:str, a3:str):
    a1_list = a1.split(',')
    a2_list = a2.split(',')
    a3_list = a3.split(',')
    for i in food_table:
        for j in a1_list:
            if j in i[1]:
                i[2] += 1
        for k in a2_list:
            if k in i[1]:
                i[2] += 1
        for l in a3_list:
            if l in i[1]:
                i[2] += 1
    return food_table

def cf_simple(user_id, food_id, food_matrix, user_similarity):
    if food_id in food_matrix:
        sim_scores = user_similarity[user_id - 1].copy()
        food_rate = food_matrix[food_id - 1].copy()
        none_eat_index = food_rate[food_rate == 0].index
        food_rate = food_rate[food_rate != 0]
        sim_scores = sim_scores.drop(none_eat_index)
        mean_rating = np.dot(sim_scores, food_rate) / np.sum(sim_scores)
    else:
        mean_rating = None
    return mean_rating

def food_recommand(id, a1, a2, a3):
    try:
        member = Member.objects.filter(member_id=id)
    except Member.DoesNotExist:
        return None
    #init
    food_size = Food.objects.all().count()
    _info = np.column_stack((Food.objects.all().values_list('food_id', 'tag'), np.zeros(food_size, int).astype(np.object)))
    _card = np.zeros((Member.objects.all().count(), food_size))
    _liked = np.array(LikeFood.objects.all().values_list('member_id', 'food_id'), int)
    _disliked = np.array(DislikeFood.objects.all().values_list('member_id', 'food_id'), int)
    _selected = np.array(SelectedFood.objects.all().values_list('member_id', 'food_id'), int)
    #좋아하는 음식 +
    for i in _liked:
        _card[i[0] - 1, i[1] - 1] += 1
    #싫어하는 음식 -
    for i in _disliked:
        _card[i[0] - 1, i[1] - 1] -= 1
    #먹었던 음식 +
    for i in _selected:
        _card[i[0] - 1, i[1] - 1] += 1
    user_similarity = cosine_similarity(_card, _card)
    user_similarity = pd.DataFrame(user_similarity, index=np.arange(_card.shape[0]), columns=np.arange(_card.shape[0]))
    food_matrix = pd.DataFrame(_card, index=np.arange(_card.shape[0]), columns=np.arange(_card.shape[1]))
    print(food_matrix)
    ret = []
    _answer = add_by_answer(_info, a1, a2, a3)
    print(_answer)
    for i in _answer[_answer[:, 2] > 0]:
        add = cf_simple(user_id=int(id), food_id=int(i[0]), food_matrix=food_matrix, user_similarity=user_similarity)
        if add != None:
            if np.isnan(add) == False:
                i[2] += add
    shuffle = np.random.permutation(_answer)
    sorted = shuffle[shuffle[:, 2].argsort()][::-1]
    print(sorted)
    for i in sorted[:4]:
        ret += Food.objects.filter(food_id=int(i[0]))
    return {"pickFood":ret}

@csrf_exempt
@api_view(['GET'])
def pickFood(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        a1 = request.GET.get('answer1', None)
        a2 = request.GET.get('answer2', None)
        a3 = request.GET.get('answer3', None)
        serializer = ResultSerializer(food_recommand(id, a1, a2, a3))
        return JsonResponse(serializer.data)

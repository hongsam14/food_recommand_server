# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Food(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=200)
    ingredient = models.CharField(max_length=200)
    youtube_url = models.CharField(max_length=200)

    class Meta:
        db_table = 'food'


class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    nick_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    picked_food_list = models.CharField(max_length=200, blank=True, null=True)
    like_food_list = models.CharField(max_length=200, blank=True, null=True)
    dislike_food_list = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'


class SelectedFood(models.Model):
    selected_food_id = models.IntegerField(primary_key=True)
    member = models.ForeignKey(Member, models.DO_NOTHING)
    food = models.ForeignKey(Food, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'selected_food'

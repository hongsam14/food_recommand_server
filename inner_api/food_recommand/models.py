# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DislikeFood(models.Model):
    dislike_food_id = models.BigIntegerField(primary_key=True)
    food = models.ForeignKey('Food', models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dislike_food'


class Food(models.Model):
    food_id = models.BigIntegerField(primary_key=True)
    ingredient = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    youtube_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'food'


class LikeFood(models.Model):
    like_food_id = models.BigIntegerField(primary_key=True)
    food = models.ForeignKey(Food, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'like_food'


class Member(models.Model):
    member_id = models.BigIntegerField(primary_key=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'


class SelectedFood(models.Model):
    select_food_id = models.BigIntegerField(primary_key=True)
    food = models.ForeignKey(Food, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(Member, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'selected_food'

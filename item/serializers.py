from django.db.models import fields
from rest_framework import serializers

from item.models import ItemModel, CategoryModel, ReviewModel


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ['id', 'title', 'tags', 'image', 'price_from', 'price_to']
        depth = 1


class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = '__all__'
        depth = 1


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'

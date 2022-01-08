from django.contrib import admin

from item.models import TagModel, ItemModel, CategoryModel, ReviewModel


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['id', 'title']


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['id', 'title']


@admin.register(ItemModel)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'district', 'phone', 'email']


@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review']


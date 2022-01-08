from django.db.models import fields
from modeltranslation.translator import register, TranslationOptions, translator

from item.models import ItemModel, TagModel, CategoryModel


class ItemTranslator(TranslationOptions):
    fields = ('description', 'mydes')
    required_languages = ('ru', 'uz')


class TagTranslator(TranslationOptions):
    fields = ('title',)
    required_languages = ('ru', 'uz')


class CategoryTranslator(TranslationOptions):
    fields = ('title',)
    required_languages = ('ru', 'uz')


translator.register(CategoryModel, CategoryTranslator)
translator.register(TagModel, TagTranslator)
translator.register(ItemModel, ItemTranslator)

from django.db import models
from django.utils.translation import ugettext_lazy as _


CATEGORIES = (
    ('programming', _('Программирование')),
    ('exact_sciences', _('Точные науки')),
    ('humanitarian_sciences', _('Гуманитарные науки')),
    ('natural_sciences', _('Естественные науки'))
)

DISTRICTS = (
    ('sergeli', _('Сергелийский район')),
    ('mirzo-ulugbek', _('Мирзо-Улугбекский район')),
    ('mirabad', _('Мирабадский район')),
    ('bektemir', _('Бектемирский район')),
    ('almazar', _('Алмазарский район')),
    ('yashnabad', _('Яшнабадский район')),
    ('yunusabad', _('Юнусабадский район')),
    ('uchtepa', _('Учтепинский район')),
    ('shayhantahur', _('Шайхантахурский район')),
    ('chilanzar', _('Чиланзарский район')),
    ('yakkasaray', _('Яккасарайский район')),
)


class TagModel(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class CategoryModel(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class ItemModel(models.Model):
    title = models.CharField(max_length=128)
    category = models.ManyToManyField(CategoryModel, related_name='items')
    price_from = models.CharField(max_length=100)
    price_to = models.CharField(max_length=100)
    district = models.CharField(max_length=64, choices=DISTRICTS)
    image = models.ImageField(upload_to='items', null=True, blank=True)
    wallpaper = models.ImageField(upload_to='wallpapers', null=True, blank=True)
    tags = models.ManyToManyField(TagModel, related_name='items')
    description = models.TextField()
    mydes = models.TextField()
    phone = models.CharField(max_length=64)
    email = models.EmailField()
    location = models.URLField(max_length=512)
    working_time = models.CharField(max_length=256)
    website = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'study center'
        verbose_name_plural = 'study centers'


class ReviewModel(models.Model):
    review = models.TextField()

    def __str__(self):
        return self.review

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
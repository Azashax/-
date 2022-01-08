from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404

from item.models import ItemModel, CategoryModel, ReviewModel
from item.serializers import ItemListSerializer, ItemDetailSerializer, CategoryListSerializer, ReviewListSerializers
from item.utils import search_product
from Users.authentication import IsAuthenticatedCustom


class ItemListView(ListAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        district = self.request.GET.get('district')
        price = self.request.GET.get('price')
        category = self.request.GET.get('category')
        items = ItemModel.objects.all()

        if district:
            items = items.filter(district=district)
        if price:
            if price == 'desc':
                items = items.order_by('-price_from')
            else:
                items = items.order_by('price_from')
        if category:
            category = category.split(',')
            items = set(items.filter(category__in=category))
        return items


class ItemSearchView(ListAPIView):
    """
    Returns a list of study centers which title corresponds to the search key

    For this add ?key={search key}
    """
    serializer_class = ItemListSerializer

    def get_queryset(self):
        key = self.request.GET.get('key')
        items = ItemModel.objects.all()
        if key:
            return search_product(key.lower(), items)
        return ItemModel.objects.none()


class ItemDetailView(RetrieveAPIView):
    """
    Returns a study center of the given id
    """
    serializer_class = ItemDetailSerializer

    def get_object(self):
        return get_object_or_404(ItemModel, pk=self.kwargs.get('pk'))


class CategoryListView(ListAPIView):
    """
    Returns a list of categories
    """
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return CategoryModel.objects.all()


class ReviewListView(ListAPIView):
    """
    Returns a list of review
    """
    serializer_class = ReviewListSerializers

    def get_queryset(self):
        return ReviewModel.objects.all()

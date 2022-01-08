from django.urls import path

from item.views import ItemListView, ItemDetailView, ItemSearchView, CategoryListView, ReviewListView

urlpatterns = [
    path('list', ItemListView.as_view(), name='list'),
    path('search', ItemSearchView.as_view(), name='search'),
    path('detail/<int:pk>', ItemDetailView.as_view(), name='detail'),
    path('category/list', CategoryListView.as_view(), name='category'),
    path('review', ReviewListView.as_view(), name='review'),
]

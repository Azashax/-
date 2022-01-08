def filter_product(search, product):
    for a in product:
        try:
            if search not in a.title.lower() and search not in a.manufacturer.title.lower():
                product = product.exclude(title=a.title)
        except AttributeError:
            if search not in a.title.lower():
                product = product.exclude(title=a.title)
    return product


def search_product(search, queryset):
    words = len(search.split())
    split = search.split()
    for word in range(words):
        search = split[word]
        queryset = filter_product(search, queryset)
    return queryset

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    # # get all product data(object)
    # query_set = Product.objects.all()
    # # for product in query_set:
    # #     print(product)
    # print(list(query_set))

    # ----
    # retrieving Objects
    # product = Product.objects.get(id=1)
    # product = Product.objects.get(pk=1)

    # -------
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass

    # -------

    # product = Product.objects.filter(pk=0).exists()
    # print(product)
    # return render(request, "hello.html", {"name": product})

    # ----------

    # Filtering Objects

    # queryset = Product.objects.filter(unit_price=20)
    # queryset = Product.objects.filter(unit_price > 20)  # NOT WROKING
    # queryset = Product.objects.filter(unit_price__gt=20)

    # [queryset api](https://docs.djangoproject.com/en/4.1/ref/models/querysets/)
    # queryset = Product.objects.filter(unit_price__range=(20,30))
    # -----

    # keyword=value
    # queryset = Product.objects.filter(collection_id=1)
    # queryset = Product.objects.filter(collection__id__range=(1, 3))
    # queryset = Product.objects.filter(title__icontains="coffee") # it check case incase sensitive
    # queryset = Product.objects.filter(last_update__year=2021)
    queryset = Product.objects.filter(description__isnull=True)

    # -------
    

    #error

    return render(request, "hello.html", {"name": queryset})

    # --------------------------------------------
    # Complex lookups Using Q Objects



# def say_hello(request):

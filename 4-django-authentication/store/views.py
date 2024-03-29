from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Product, Collection, OrderItem, Reviews, Cart, CartItem
from .filters import ProductFilter
from .serializers import (
    ProductSerializers,
    CollectionSerializers,
    ReviewsSerializers,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)


# TODO ViewSets

# productList , productDetails in one class
"""class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializers

    def get_serializer_context(self):
        return {"request": self.request}

    # delete method for delete all list and one object also
    def destroy(self, request, *args, **kwargs):  # delete one objects
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count():
            return Response({"error": "Product cannot be deleted."})
        return super().destroy(request, *args, **kwargs)"""


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count("product")).all()
    serializer_class = CollectionSerializers

    # delete method for delete all list and one object also
    # def destroy(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.product_set.count() > 0:
    #         return Response({"error": "Product cannot be deleted."})
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response({"error": "Product cannot be deleted."})
        return super().destroy(request, *args, **kwargs)


# TODO Building the Reviews API

"localhost:8000/store/products/1/reviews/"
"localhost:8000/store/products/1/reviews/1/"

# - create a model class
# - create a migrations
# -apply the migrations

# - create a serializer
# - create a view
# - register a route


class ReviewsViewSet(ModelViewSet):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializers

    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs["products_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["products_pk"]}


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    search_fields = ["^title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    """REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "PAGE_SIZE": 10,
    }"""

    def get_serializer_context(self):
        return {"request": self.request}

    # delete method for delete all list and one object also
    def destroy(self, request, *args, **kwargs):  # delete one objects
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count():
            return Response({"error": "Product cannot be deleted."})
        return super().destroy(request, *args, **kwargs)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related("cartitem_set__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    # queryset = CartItem.objects.all()
    # serializer_class = CartItemSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return (
            CartItem.objects.filter(cart_id=self.kwargs["carts_pk"])
            .select_related("product")
            .all()
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["carts_pk"]}

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from .models import Category, Product, Review
from .permissions import IsAdminPermission#, IsAuthorPermission
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductsListSerializer



class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['title']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminPermission]
        # elif self.action == 'like':
        #     permissions = [IsAuthenticated]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_class(self):#нужен для разделения листинга и деталей товара
        if self.action == 'list':
            return ProductsListSerializer
        return self.serializer_class

# /api/v1/posts/slug/
#/api/v1/posts/slug/comments
    @action(['GET'], detail=True)
    def reviews(self, request, slug=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action == 'create':
    #         permissions = [IsAdminPermission]
    #     elif self.action in ['update', 'partial_update', 'destroy']:
    #         permissions = [IsAuthorPermission]
    #     elif self.action == 'like':
    #         permissions = [IsAuthenticated]
    #     else:
    #         permissions = []
    #     return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product-list', request=request, format=format),
        'categories': reverse('categories-list', request=request, format=format),
    })


class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.none()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]







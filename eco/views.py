from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products related to a specific category."""
        category = self.get_object()
        products = category.product_set.all()  # Use the reverse relationship to get products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']  # Fields to search on
    


# views.py

class SearchPagination(PageNumberPagination):
    page_size = 12  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class SearchView(APIView):
    pagination_class = SearchPagination

    def get(self, request):
        # Get search parameters
        query = request.query_params.get('q', '')
        category_id = request.query_params.get('category', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        sort_by = request.query_params.get('sort_by', 'created_at')

        if not query and not category_id:
            return Response(
                {'error': 'Please provide a search query or category'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize queries
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()

        # Apply search if query exists
        if query:
            products = Product.search(query)
            categories = Category.search(query)

        # Apply category filter
        if category_id:
            products = products.filter(category_id=category_id)

        # Apply price filters
        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # Apply sorting
        if sort_by == 'price_low':
            products = products.order_by('price')
        elif sort_by == 'price_high':
            products = products.order_by('-price')
        elif sort_by == 'name':
            products = products.order_by('name')
        else:
            products = products.order_by('-created_at')

        # Paginate products
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)

        # Serialize the results
        product_serializer = ProductSerializer(paginated_products, many=True)
        category_serializer = CategorySerializer(categories, many=True)

        return Response({
            'products': {
                'results': product_serializer.data,
                'count': products.count(),
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link()
            },
            'categories': category_serializer.data
        })
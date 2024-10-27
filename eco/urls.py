from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'eco'

# auth urls

urlpatterns = [

]

# urls

router = DefaultRouter()


router.register('products',views.ProductViewSet,basename='products')
router.register('categories',views.CategoryViewSet,basename='categories')



# app urls
urlpatterns += [
    path('search', views.SearchView.as_view(), name='search'),  # Removed trailing slash

] + router.urls

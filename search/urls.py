from django.urls import path
from .views import ProductSearchView, ProductSuggestView

urlpatterns = [
    path("search/products/", ProductSearchView.as_view()),
    path("search/suggest/", ProductSuggestView.as_view()),
]
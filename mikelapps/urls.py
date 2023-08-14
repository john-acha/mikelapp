"""Defines URL patterns for mikelapps."""

from django.urls import path

from . import views

app_name = 'mikelapps'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all products.
    path('products/', views.products, name='products'),
    # Detail page for a single product.
    path('products/<int:product_id>/', views.product, name='product'),
    # Page for adding a new product.
    path('new_product/', views.new_product, name='new_product'),
    # Page for adding a new entry.
    path('new_entry/<int:product_id>/', views.new_entry, name='new_entry'),
    # Page for editing an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
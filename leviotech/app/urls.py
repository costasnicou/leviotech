from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage' ),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'), 
    path('category/<slug:slug>/', views.category_detail, name='category_detail'), 
    path('page/<slug:slug>/', views.page_detail, name='page_detail'), 
   
]
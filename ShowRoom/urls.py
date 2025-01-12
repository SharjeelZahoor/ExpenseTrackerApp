from django.urls import path
from . import views


urlpatterns=[
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),
    path('compare/', views.compare, name="compare"),
    path('register/', views.register, name="register"),
    path('products/', views.products, name="products"),
    path('add-mobile/', views.addMobile, name="add-mobile"),
    path('add-review/', views.addReview, name="add-review"),
    path('update-product/<str:pk>/', views.updateMobile, name="update-product"),
    path('upload-product-photo/<str:pk>/', views.uploadMobilePhoto, name="upload-product-photo"),
    path('product/<str:pk>/', views.product, name="product"),
    path('add-mobile-photo/<str:pk>/', views.addMobilePhoto, name="add-mobile-photo"),
    path('add-to-wishlist/<str:pk>/', views.addToWishList, name="add-to-wishlist"),
    path('del-from-wishlist/<str:pk>/', views.removeWishList, name="del-from-wishlist"),
    path('add-to-compare/<str:pk>/', views.addToCompare, name="add-to-compare"),
    path('rem-from-compare/<str:pk>/', views.remFromCompare, name="rem-from-compare"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('brands/', views.brands, name="brands"),
    path('add-brand/', views.addBrand, name="add-brand"),
    path('upload-brand-photo/<str:pk>/', views.uploadBrandPhoto, name="upload-brand-photo"),
    path('update-brand/<str:pk>/', views.updateBrand, name="update-brand"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),



    # path('cars/', views.cars, name="cars"),
    # path('add-car/', views.addCar, name="add-car"),
    # path('update-car/<str:pk>/', views.updateCar, name="update-car"),
    # path('upload-car-photo/<str:pk>/', views.uploadCarPhoto, name="upload-car-photo"),
    # path('companies/', views.companies, name="companies"),
    # path('add-company/', views.addCompany, name="add-company"),
    # path('update-company/<str:pk>/', views.updateCompany, name="update-company"),
    # path('upload-company-photo/<str:pk>/', views.uploadCompanyPhoto, name="upload-company-photo"),
]
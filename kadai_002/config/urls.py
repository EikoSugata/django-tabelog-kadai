"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #管理者ページ
    path('admin/', admin.site.urls),

    # トップページ
    path('', views.IndexListView.as_view()),

    # Restaurant
    path('categories/<str:pk>/', views.CategoryListView.as_view()),
    path('restaurants/<str:pk>/', views.RestaurantDetailView.as_view()),
    path('restaurants/', views.RestaurantListView.as_view()),
    
    # Reserve
    path('reserve/add/<str:pk>/', views.ReserveCreateView.as_view()),
    path('reserve/', views.ReserveListView.as_view()),
    path('reserve/delete/<str:pk>/', views.ReserveDeleteView.as_view()),

    # Favorite
    path('favorite/add/<str:pk>/', views.FavoriteCreateView.as_view()),
    path('favorite/delete/<str:pk>/', views.FavoriteDeleteView.as_view()),
    path('favorite/', views.FavoriteListView.as_view()),
    
    # Review
    path('review/add/<str:pk>/', views.ReviewCreateView.as_view()),
    path('review/delete/<str:pk>/', views.ReviewDeleteView.as_view()),

    # Account
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('account/', views.AccountUpdateView.as_view()),
    path('password/', views.PasswordChange.as_view()),

    # Pay
    path('pay/upgrade/', views.PayWithStripe.as_view()),
    path('pay/success/', views.PaySuccessView.as_view()),
    path('pay/cancel/', views.PayCancelView.as_view()),
    path('pay/downgrade/', views.CancelWithStripeView.as_view()),

    # Order
    path('orders/', views.OrderListView.as_view()),
]

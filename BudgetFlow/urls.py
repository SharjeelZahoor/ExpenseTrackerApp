from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    # User Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # Expense Management
    path('add-expense/', views.add_expense, name="add-expense"),
    path('edit-expense/<int:pk>/', views.edit_expense, name="edit-expense"),
    path('delete-expense/<int:pk>/', views.delete_expense, name="delete-expense"),
    path('expenses/', views.expense_list, name="expenses"),
    path('budgets/', views.budget_list, name='budgets'),

    # Category Management
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # BUdget Urls
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/edit/<int:pk>/', views.budget_update, name='budget_update'),
    path('budgets/delete/<int:pk>/', views.budget_delete, name='budget_delete'),

    #TRANSACTIONS
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/edit/<int:pk>/', views.transaction_update, name='transaction_update'),
    path('transactions/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),

    #Alert
    path('alerts/', views.alerts_view, name='alerts'),
    path('alerts/read/<int:id>/', views.mark_as_read, name='mark_alert_as_read'),
    path('alerts/unread/<int:id>/', views.mark_as_unread, name='mark_alert_as_unread'),
    path('alerts/delete/<int:id>/', views.delete_alert, name='delete_alert'),

    # Reports & Filtering
    path('search/', views.search_expenses, name="search"),
    path('report/', views.report, name="report"),

    # Profile
    path('profile/', views.profile, name="profile"),
]

from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import chart_data
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name="home"),
    # User Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
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

    # ✅ Chart-related URLs
    path('charts/', login_required(TemplateView.as_view(template_name="BudgetFlow/charts.html")), name='charts'),
    path('charts/data/', chart_data, name='chart_data'),

    # ✅ NEW Financial Summary & CSV Export
    path('summary/', views.summary_page, name='summary_page'),  # <- This is the fix
    path('api/summary/', views.financial_summary, name='financial_summary'),
    path('export/csv/', views.export_csv, name='export_csv'),
    
    # Reports & Filtering
    path('search/', views.search_expenses, name="search"),
    path('report/', views.report, name="report"),

    # Profile
    path('profile/', views.profile, name="profile"),

]

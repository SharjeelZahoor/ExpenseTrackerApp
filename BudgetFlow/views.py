from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum
from datetime import date
from django.db import transaction
from .forms import TransactionForm, EditTransactionForm, CategoryForm, BudgetForm, UserRegisterForm
from .models import Transaction, Category, Budget, Alert
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import calendar
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
import csv


title = 'ExpenseTrackerProject'


                                    #home view


@login_required(login_url='login')
def home(request):
    user = request.user
    page = 'Home'
    sub_page = 'Dashboard'
    pgTitle = f"{page} | {sub_page}"

    today = date.today()
    current_month = today.month
    current_year = today.year

    # Fetch all transactions ordered by date
    full_transactions = Transaction.objects.filter(user=user).order_by('-date')
    transactions = full_transactions[:10]

    # Monthly transactions
    monthly_transactions = full_transactions.filter(date__month=current_month, date__year=current_year)

    total_income = monthly_transactions.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = monthly_transactions.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # Current month budgets
    current_month_budgets = Budget.objects.filter(user=user, month=current_month, year=current_year)

    budget_progress = []

    for budget in current_month_budgets:
        spent = Transaction.objects.filter(
            user=user,
            type='Expense',
            category=budget.category,
            date__month=current_month,
            date__year=current_year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        percent_used = (spent / budget.amount) * 100 if budget.amount else 0

        # Trigger alert if 80% usage crossed and not already alerted
        if percent_used >= 80:
            alert_message = f"Warning: You have used {round(percent_used)}% of your budget for '{budget.category.name}' this month."
            if not Alert.objects.filter(user=user, message=alert_message, is_read=False).exists():
                Alert.objects.create(user=user, message=alert_message)

        budget_progress.append({
            'category': budget.category.name,
            'amount': budget.amount,
            'spent': spent,
            'percent_used': round(percent_used, 2)
        })

    # Fetch unread alerts
    alerts = Alert.objects.filter(user=request.user, is_read=False)

    context = {
        'page': page,
        'sub_page': sub_page,
        'pgTitle': pgTitle,
        'transactions': transactions,
        'income': total_income,
        'expense': total_expense,
        'balance': balance,
        'budgets': current_month_budgets,
        'budget_progress': budget_progress,
        'alerts': alerts,
    }

    return render(request, 'BudgetFlow/home.html', context)


                                #Authentication Views

#register
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
                return redirect('register')

            # if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered. Please use a different one.')
                return redirect('register')

            # Create the user manually
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Redirect to login after successful registration
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user) 
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


# Logout
@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')




                                # Category views


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'BudgetFlow/category_list.html', {'categories': categories, 'page': 'Categories'})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'BudgetFlow/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'BudgetFlow/category_form.html', {'form': form, 'title': 'Edit Category'})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'BudgetFlow/category_confirm_delete.html', {'category': category})




                            # Transaction Views


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    categories = Category.objects.all()

    # Get filters from GET params
    keyword = request.GET.get('keyword', '').strip()
    category_id = request.GET.get('category_id')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    amount_min = request.GET.get('amount_min')
    amount_max = request.GET.get('amount_max')
    sort_by = request.GET.get('sort_by', 'date_desc')

    # Apply keyword filter
    if keyword:
        transactions = transactions.filter(Q(description__icontains=keyword))

    # Apply category filter
    if category_id:
        transactions = transactions.filter(category_id=category_id)

    # Apply date range filter
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)

    # Apply amount range filter
    if amount_min:
        transactions = transactions.filter(amount__gte=amount_min)
    if amount_max:
        transactions = transactions.filter(amount__lte=amount_max)

    # Sorting
    if sort_by == 'date_asc':
        transactions = transactions.order_by('date')
    elif sort_by == 'amount_asc':
        transactions = transactions.order_by('amount')
    elif sort_by == 'amount_desc':
        transactions = transactions.order_by('-amount')
    else:  # default
        transactions = transactions.order_by('-date')

    context = {
        'transactions': transactions,
        'categories': categories,
        'selected_category_id': category_id,
        'current_sort': sort_by,
        'keyword': keyword,
        'date_from': date_from,
        'date_to': date_to,
        'amount_min': amount_min,
        'amount_max': amount_max,
        'page': 'Transactions',
    }

    return render(request, 'BudgetFlow/transaction_list.html', context)


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully.")
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'BudgetFlow/transaction_form.html', {'form': form, 'title': 'Add Transaction'})


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EditTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            return redirect('transaction_list')
    else:
        form = EditTransactionForm(instance=transaction)
    return render(request, 'BudgetFlow/transaction_form.html', {'form': form, 'title': 'Edit Transaction'})


# ✅ Delete a transaction
@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted successfully.")
        return redirect('transaction_list')
    return render(request, 'BudgetFlow/transaction_confirm_delete.html', {'transaction': transaction})




                            # Budget View


@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')
    return render(request, 'BudgetFlow/budget_list.html', {'budgets': budgets, 'page': 'Budgets'})


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully.')
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'BudgetFlow/budget_form.html', {'form': form, 'title': 'Add Budget'})


@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully.')
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'BudgetFlow/budget_form.html', {'form': form, 'title': 'Edit Budget'})


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully.')
        return redirect('budget_list')
    return render(request, 'BudgetFlow/budget_confirm_delete.html', {'budget': budget})




                                # Alert Views



from django.db.models import Max, Subquery, OuterRef

@login_required
def alerts_view(request):
    with transaction.atomic():
        # Step 1: Remove duplicate alerts (keep only latest one per message)
        duplicates = (
            Alert.objects.filter(user=request.user)
            .values('message')
            .annotate(max_id=Max('id'), msg_count=Count('id'))
            .filter(msg_count__gt=1)
        )

        for entry in duplicates:  # <-- FIXED LINE
            message = entry['message']
            max_id = entry['max_id']
            Alert.objects.filter(user=request.user, message=message).exclude(id=max_id).delete()

    # Step 2: Show only latest alerts per message
    latest_ids = Alert.objects.filter(user=request.user).values('message').annotate(
        latest_id=Max('id')
    ).values_list('latest_id', flat=True)

    alerts = Alert.objects.filter(id__in=latest_ids).order_by('-created_at')

    return render(request, 'BudgetFlow/alert.html', {'alerts': alerts, 'page': 'Alerts'})


@login_required
def mark_as_read(request, id):
    alert = get_object_or_404(Alert, id=id)
    alert.is_read = True
    alert.save()
    return redirect('alerts')  

@login_required
def mark_as_unread(request, id):
    alert = get_object_or_404(Alert, id=id)
    alert.is_read = False
    alert.save()
    return redirect('alerts')  

@login_required
def delete_alert(request, id):
    alert = get_object_or_404(Alert, id=id)
    alert.delete()
    return redirect('alerts') 



                            
                            # expense charts view

                            
@login_required
def chart_data(request):
    user = request.user

    category_data = (
        Transaction.objects.filter(user=user, type='Expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    monthly_data = (
        Transaction.objects.filter(user=user, type='Expense')
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Format for frontend
    category_labels = [item['category__name'] for item in category_data]
    category_totals = [float(item['total']) for item in category_data]

    month_labels = [item['month'].strftime('%b %Y') for item in monthly_data]
    month_totals = [float(item['total']) for item in monthly_data]

    return JsonResponse({
        'category': {
            'labels': category_labels,
            'data': category_totals,
        },
        'monthly': {
            'labels': month_labels,
            'data': month_totals,
        }
    })




                        #summary page and financial summaries


@login_required
def summary_page(request):
    months_range = list(calendar.month_name)[1:13]  # ['January', ..., 'December']
    return render(request, 'BudgetFlow/summary.html', {'months_range': months_range})


@login_required
@csrf_exempt
def financial_summary(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    user = request.user
    queryset = Transaction.objects.filter(user=user)  # ✅ Filter by logged-in user

    if year:
        queryset = queryset.filter(date__year=year)
    if month:
        try:
            month_number = list(calendar.month_name).index(month)
            queryset = queryset.filter(date__month=month_number)
        except ValueError:
            return JsonResponse({'error': 'Invalid month provided'}, status=400)

    total_income = queryset.filter(type__iexact='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = queryset.filter(type__iexact='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    top_categories = queryset.values('category__name').annotate(total=Sum('amount')).order_by('-total')[:5]
    top_data = {item['category__name']: item['total'] for item in top_categories}

    return JsonResponse({
        'month': month,
        'year': year,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'top_categories': top_data
    })




                            #Download CSV file


def export_csv(request):
    transactions = Transaction.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=transactions.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount', 'Type', 'Description']) 
    
    for tx in transactions:
        writer.writerow([
            tx.date,
            tx.category.name if tx.category else "Uncategorized",
            tx.amount,
            tx.type,
            tx.description or ""  
        ])
    
    return response
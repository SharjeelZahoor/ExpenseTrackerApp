from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum
from datetime import date
from .forms import TransactionForm, EditTransactionForm, CategoryForm, BudgetForm, UserRegisterForm
from .models import Transaction, Category, Budget, Alert
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect


title = 'ExpenseTrackerProject'



#home view
@login_required(login_url='login')
def home(request):
    user = request.user
    page = 'Home'
    sub_page = 'Dashboard'
    pgTitle = f"{page} | {sub_page}"

    # Transactions
    full_transactions = Transaction.objects.filter(user=user).order_by('-date')
    transactions = full_transactions[:10]

    total_income = full_transactions.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = full_transactions.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # All Budgets
    budgets = Budget.objects.filter(user=user)

    # Current Month & Year
    today = date.today()
    current_month_budgets = budgets.filter(month=today.month, year=today.year)

    budget_progress = []
    for budget in current_month_budgets:
        spent = Transaction.objects.filter(
            user=user,
            type='Expense',
            category=budget.category,
            date__month=budget.month,
            date__year=budget.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        percent_used = (spent / budget.amount) * 100 if budget.amount else 0

        # ✅ Auto-create alert if 80% usage crossed and alert not already shown
        if percent_used >= 80:
            alert_message = f"Warning: You have used {round(percent_used)}% of your budget for '{budget.category.name}' this month."
            already_alerted = Alert.objects.filter(
                user=user,
                message=alert_message,
                is_read=False
            ).exists()
            if not already_alerted:
                Alert.objects.create(user=user, message=alert_message)

        budget_progress.append({
            'category': budget.category.name,
            'amount': budget.amount,
            'spent': spent,
            'percent_used': round(percent_used, 2)
        })

    # Fetch unread alerts
    alerts = Alert.objects.filter(user=user, is_read=False)

    context = {
        'page': page,
        'sub_page': sub_page,
        'pgTitle': pgTitle,
        'transactions': transactions,
        'income': total_income,
        'expense': total_expense,
        'balance': balance,
        'budgets': budgets,
        'budget_progress': budget_progress,
        'alerts': alerts,
    }

    return render(request, 'BudgetFlow/home.html', context)


#register
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another one.')
                return redirect('register')

            # Check if the email already exists
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
        username = request.POST.get('username')  # Use 'username' as input name from the form
        password = request.POST.get('password')  # Use 'password' as input name from the form
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Log the user in
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


# Logout
@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


# Expense List
@login_required
def expense_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'BudgetFlow/expense_list.html', {'transactions': transactions})


# Add Expense
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('expenses')
    else:
        form = TransactionForm()
    return render(request, 'BudgetFlow/add_expense.html', {'form': form})


# Edit Expense
@login_required
def edit_expense(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expenses')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'BudgetFlow/edit_expense.html', {'form': form})


# Delete Expense
@login_required
def delete_expense(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('expenses')



# ✅ List all categories
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'BudgetFlow/category_list.html', {'categories': categories})

# ✅ Create a new category
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

# ✅ Update an existing category
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

# ✅ Delete a category
@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'BudgetFlow/category_confirm_delete.html', {'category': category})


# Search Expenses
@login_required
def search_expenses(request):
    transactions = Transaction.objects.filter(user=request.user)
    query = request.GET.get('q')
    if query:
        transactions = transactions.filter(
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'BudgetFlow/expense_list.html', {'transactions': transactions})


# Budget Report
@login_required
def report(request):
    user = request.user
    selected_month = int(request.GET.get('month', date.today().month))
    selected_year = int(request.GET.get('year', date.today().year))

    budgets = Budget.objects.filter(user=user, month=selected_month, year=selected_year)
    transactions = Transaction.objects.filter(user=user, date__month=selected_month, date__year=selected_year)

    report_data = []
    for budget in budgets:
        spent = transactions.filter(category=budget.category, type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        report_data.append({
            'category': budget.category.name,
            'budgeted': budget.amount,
            'spent': spent,
            'remaining': budget.amount - spent
        })

    context = {
        'report_data': report_data,
        'selected_month': selected_month,
        'selected_year': selected_year
    }
    return render(request, 'BudgetFlow/report.html', context)



# ✅ List all transactions
@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'BudgetFlow/transaction_list.html', {'transactions': transactions})

# ✅ Create a transaction
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

# ✅ Update a transaction
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


# Profile
@login_required
def profile(request):
    return render(request, 'BudgetFlow/profile.html', {'user': request.user})


# Budget Views
# ✅ List all budgets for the logged-in user
@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')
    return render(request, 'BudgetFlow/budget_list.html', {'budgets': budgets})

# ✅ Create a new budget
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

# ✅ Update an existing budget
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

# ✅ Delete a budget
@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully.')
        return redirect('budget_list')
    return render(request, 'BudgetFlow/budget_confirm_delete.html', {'budget': budget})




 #  Alert views
@login_required
def alerts_view(request):
    # Get alerts for the logged-in user
    alerts = Alert.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'BudgetFlow/alert.html', {'alerts': alerts})


@login_required
def mark_as_read(request, id):
    alert = get_object_or_404(Alert, id=id)
    alert.is_read = True
    alert.save()
    return redirect('alerts')  # Redirect back to the alerts page

@login_required
def mark_as_unread(request, id):
    alert = get_object_or_404(Alert, id=id)
    alert.is_read = False
    alert.save()
    return redirect('alerts')  # Redirect back to the alerts page

@login_required
def delete_alert(request, id):
    alert = get_object_or_404(Alert, id=id)
    alert.delete()
    return redirect('alerts')  # Re
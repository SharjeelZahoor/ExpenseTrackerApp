from django.db import models
from django.contrib.auth.models import User


# ✅ Category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ Transaction model (for both expenses and incomes)
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.amount} on {self.date}"


# ✅ Budget model (monthly budget by category)
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveIntegerField()  # 1 = Jan, 12 = Dec
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.category.name} - {self.amount} for {self.month}/{self.year}"


# ✅ Alert model (for budget threshold notifications)
class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.user.username}: {'Read' if self.is_read else 'Unread'}"

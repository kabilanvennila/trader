from django.db import models
from django.utils import timezone

class Trade(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    ]

    indices_stock = models.CharField(max_length=50)
    bias = models.CharField(max_length=20)
    setup = models.CharField(max_length=100)
    strategy = models.CharField(max_length=100)
    days_to_expiry = models.CharField(max_length=50)
    main_lots = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    hedge_lots = models.PositiveIntegerField(null=True, blank=True)
    price_per_hedge_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_profit = models.DecimalField(max_digits=12, decimal_places=2)
    max_loss = models.DecimalField(max_digits=12, decimal_places=2)
    capital = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.indices_stock} | {self.strategy} | {self.status}"


class Strike(models.Model):
    trade = models.ForeignKey(Trade, related_name="strikes", on_delete=models.CASCADE)
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    option_type = models.CharField(max_length=2, choices=[("CE", "Call"), ("PE", "Put")])
    position = models.CharField(max_length=4, choices=[("B", "Buy"), ("S", "Sell")])
    lots = models.PositiveIntegerField(default=1)
    expiry_date = models.DateField() 
    ltp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 

    def __str__(self):
        return f"{self.position} {self.option_type} {self.strike_price} ({self.expiry_date})"

class Transfer(models.Model):
    TRANSFER_TYPES = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
    ]

    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=20, choices=TRANSFER_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.type} - ₹{self.amount}"

    @staticmethod
    def get_summary():
        deposits = Transfer.objects.filter(type="DEPOSIT").aggregate(total=models.Sum("amount"))["total"] or 0
        withdrawals = Transfer.objects.filter(type="WITHDRAWAL").aggregate(total=models.Sum("amount"))["total"] or 0
        total_capital = deposits - withdrawals
        return {
            "total_capital": total_capital,
            "total_deposits": deposits,
            "total_withdrawals": withdrawals,
        }

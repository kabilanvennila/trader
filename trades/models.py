from django.db import models

class Trade(models.Model):
    INDICES = [
        ("NIFTY", "Nifty 50"),
        ("BANKNIFTY", "Bank Nifty"),
        ("STOCK", "Stock"),
    ]

    BIAS_CHOICES = [
        ("BULLISH", "Bullish"),
        ("BEARISH", "Bearish"),
        ("NEUTRAL", "Neutral"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    ]

    indices_stock = models.CharField(max_length=50, choices=INDICES)
    bias = models.CharField(max_length=20, choices=BIAS_CHOICES)
    setup = models.CharField(max_length=100)
    strategy = models.CharField(max_length=100)
    days_to_expiry = models.CharField(max_length=50)  # e.g. "This Week"
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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.indices_stock} | {self.strategy} | {self.status}"

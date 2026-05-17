# marketing/models.py\

#with database
from django.db import models

class CustomerPrediction(models.Model):
    # Demographics & Account
    Age = models.IntegerField()
    Income = models.FloatField()
    Tenure_Days = models.IntegerField()
    
    # Spending Amounts
    MntWines = models.FloatField()
    MntFruits = models.FloatField()
    MntMeatProducts = models.FloatField()
    MntFishProducts = models.FloatField()
    MntSweetProducts = models.FloatField()
    MntGoldProds = models.FloatField()
    Total_Spent = models.FloatField()

    # Purchasing Behavior
    NumCatalogPurchases = models.IntegerField()
    NumStorePurchases = models.IntegerField()
    NumWebVisitsMonth = models.IntegerField()
    Recency = models.IntegerField()
    Prev_Campaigns = models.IntegerField()

    # The Final Output & Timestamp
    prediction_result = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Customer {self.id} - {self.created_at.strftime('%Y-%m-%d')}"
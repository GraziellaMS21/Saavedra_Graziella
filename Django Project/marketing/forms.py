# # marketing/forms.py
# from django import forms

# class MarketingPredictionForm(forms.Form):
#     Age = forms.IntegerField(label='Customer Age', min_value=18)
#     Income = forms.FloatField(label='Annual Income')
#     Tenure_Days = forms.IntegerField(label='Tenure (in Days)')
    
#     MntWines = forms.FloatField(label='Amount Spent on Wines')
#     MntFruits = forms.FloatField(label='Amount Spent on Fruits')
#     MntMeatProducts = forms.FloatField(label='Amount Spent on Meat Products')
#     MntFishProducts = forms.FloatField(label='Amount Spent on Fish Products')
#     MntSweetProducts = forms.FloatField(label='Amount Spent on Sweet Products')
#     MntGoldProds = forms.FloatField(label='Amount Spent on Gold Products')
#     Total_Spent = forms.FloatField(label='Total Amount Spent (All Categories)')

#     NumCatalogPurchases = forms.IntegerField(label='Number of Catalog Purchases')
#     NumStorePurchases = forms.IntegerField(label='Number of Store Purchases')
#     NumWebVisitsMonth = forms.IntegerField(label='Web Visits per Month')
#     Recency = forms.IntegerField(label='Recency (Days since last purchase)')
#     Prev_Campaigns = forms.IntegerField(label='Previous Campaigns Accepted')

# with database
# marketing/forms.py
from django import forms
from .models import CustomerPrediction

class MarketingPredictionForm(forms.ModelForm):
    class Meta:
        model = CustomerPrediction
        # We don't want the user to type in the result or timestamp, so we exclude them
        exclude = ['prediction_result', 'created_at']
        
        # We can still apply custom labels here
        labels = {
            'Age': 'Customer Age',
            'Income': 'Annual Income',
            'Tenure_Days': 'Tenure (in Days)',
            'MntWines': 'Amount Spent on Wines',
            'MntFruits': 'Amount Spent on Fruits',
            'MntMeatProducts': 'Amount Spent on Meat Products',
            'MntFishProducts': 'Amount Spent on Fish Products',
            'MntSweetProducts': 'Amount Spent on Sweet Products',
            'MntGoldProds': 'Amount Spent on Gold Products',
            'Total_Spent': 'Total Amount Spent (All Categories)',
            'NumCatalogPurchases': 'Number of Catalog Purchases',
            'NumStorePurchases': 'Number of Store Purchases',
            'NumWebVisitsMonth': 'Web Visits per Month',
            'Recency': 'Recency (Days since last purchase)',
            'Prev_Campaigns': 'Previous Campaigns Accepted',
        }
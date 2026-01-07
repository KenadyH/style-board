from django import forms
from .models import OutfitPlan, LookItem

class OutfitPlanForm(forms.ModelForm):
    class Meta:
        model = OutfitPlan
        fields = ['date', 'title', 'mood', 'occasion']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class LookItemForm(forms.ModelForm):
    class Meta:
        model = LookItem
        fields = ["image", "category"]
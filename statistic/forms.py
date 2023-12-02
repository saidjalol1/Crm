from main.models import Expenses
from django import forms


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'start_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'end_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }
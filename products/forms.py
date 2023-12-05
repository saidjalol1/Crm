from django import forms
from .models import Product

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['tag']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'net_profit':forms.NumberInput(attrs={'class':'form-control'}),
            'body_price':forms.NumberInput(attrs={'class':'form-control'}),
            'old_price':forms.NumberInput(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'discount':forms.NumberInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control-file'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'storage':forms.Select(attrs={'class':'form-control'}),
            # 'tag':forms.Select(attrs={'class':'form-control'}),
        }
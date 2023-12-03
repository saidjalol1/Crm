from django import forms
from .models import Orders, Deliver, Staffs

class DriverForm(forms.ModelForm):
    class Meta:
        model = Deliver
        fields = '__all__'


class StaffsForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'Ismi'}),
            'phone_number':forms.TextInput(attrs={'placeholder':'Telefon raqami'}),
            'address':forms.TextInput(attrs={'placeholder':'Manzil'}),
            'salary':forms.NumberInput(attrs={'placeholder':'Oylik'}),
            'position':forms.NumberInput(attrs={'placeholder':'Lavozimi'}),
        }
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
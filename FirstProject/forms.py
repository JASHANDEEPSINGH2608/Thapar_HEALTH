from django import forms
from .models import data
class dataForm(forms.ModelForm):
    class Meta:
        model= data
        fields=['profile_image', 'Mobile_number','Birthday','Medical_Allergies'] 


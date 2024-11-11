from django import forms
from .models import PatientToken, User, AvailableTime


class TokenForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=AvailableTime.objects.all())
    class Meta:
        model = PatientToken
        fields = ['doctor', 'name', 'phone_no', 'token_no', 'date', 'time']
        
    
class TokenDetailsForm(forms.ModelForm):
    class Meta:
        model = AvailableTime
        fields = ['doctor', 'available_date', 'available_time']
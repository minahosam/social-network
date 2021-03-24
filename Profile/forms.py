from django import forms
from .models import profile
class profile_form(forms.ModelForm):
    class Meta:
        model = profile
        #fields = '__all__'
        exclude=['user','friends','slug']
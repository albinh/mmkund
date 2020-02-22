from django import forms
from kunder.models import Customer
from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label="Din e-post")
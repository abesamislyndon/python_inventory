from django import forms
from .models import Client
import uuid



class ClientForm(forms.ModelForm):
   
    class Meta:
        model  = Client
        fields  = '__all__'
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight',
                'placeholder' : 'Client Name'
            }) ,

             'guest_count': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight',
                'placeholder' : 'Guest Count'
            }) ,
            'client_url': forms.HiddenInput(attrs={
            'value': str(uuid.uuid4())  # Set the default value of the hidden field as a UUID string
        }),
        }
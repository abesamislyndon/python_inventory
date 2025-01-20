from django import forms
from .models import Client, ClientMsg
import uuid

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight',
                'placeholder': 'Client Name',
            }),
            'guest_count': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight',
                'placeholder': 'Guest Count',
            }),
            'client_url': forms.HiddenInput(attrs={
                'value': str(uuid.uuid4())  # Set a default UUID value
            }),
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = ClientMsg
        fields = ['guest_name', 'content', 'image']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight',
                'placeholder': 'Your Name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight',
                'placeholder': 'Your Message',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-gray-700 py-2 px-3 border rounded',
            }),
        }




class MessageBoardForm(forms.ModelForm):
    event_logo = forms.ImageField(
        required=False,
        label="Event Logo",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )
    theme_color = forms.CharField(
        required=False,
        label="Theme Color",
        widget=forms.TextInput(attrs={"type": "color", "class": "form-control mt-2 mb-2"}),
    )

    class Meta:
        model = Client
        fields = ["event_logo", "theme_color"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate the theme_color field from theme_settings if available
        if self.instance and self.instance.theme_settings:
            self.fields["theme_color"].initial = self.instance.theme_settings.get("theme_color", "#FF5733")

    def clean(self):
        cleaned_data = super().clean()
        theme_color = cleaned_data.get("theme_color")

        # Validate or set a default theme color
        if not theme_color:
            theme_color = "#FF5733"  # Default color
        cleaned_data["theme_color"] = theme_color

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        theme_color = self.cleaned_data.get("theme_color", "#FF5733")

        # Update theme_settings with the selected color
        instance.theme_settings = {"theme_color": theme_color}

        if commit:
            instance.save()
        return instance
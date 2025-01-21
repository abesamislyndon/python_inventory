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
        widget=forms.ClearableFileInput(attrs={"class": "bg-[#f3f3f3] mt-5"}),
    )
    
    theme_color = forms.CharField(
        required=False,
        label="Theme Color",
        widget=forms.TextInput(attrs={"type": "color", "class": "form-control mt-2 mb-2"}),
    )
    
    card_color = forms.CharField(
        required=False,
        label="Card Color",
        widget=forms.TextInput(attrs={"type": "color", "class": "form-control mt-2 mb-2"}),
    )

    class Meta:
        model = Client
        fields = ["event_logo", "theme_color", "card_color"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate the theme_color and card_color fields from theme_settings if available
        if self.instance and self.instance.theme_settings:
            self.fields["theme_color"].initial = self.instance.theme_settings.get("theme_color", "#FF5733")
            self.fields["card_color"].initial = self.instance.theme_settings.get("card_color", "#000000")

    def clean(self):
        cleaned_data = super().clean()
        theme_color = cleaned_data.get("theme_color")
        card_color = cleaned_data.get("card_color")

        # Validate or set default colors
        if not theme_color:
            theme_color = "#FF5733"  # Default theme color
        if not card_color:
            card_color = self.get_lighter_color(theme_color, percent=0.7)  # Calculate even lighter card color if not provided

        cleaned_data["theme_color"] = theme_color
        cleaned_data["card_color"] = card_color

        return cleaned_data

    def get_lighter_color(self, hex_color, percent=0.7):
        """Function to lighten a color by a given percentage"""
        # Remove the '#' and convert the hex string into RGB values
        hex_color = hex_color.lstrip('#')
        r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

        # Increase RGB values by the percentage, ensuring it doesn't go over 255
        r = min(255, int(r + (255 - r) * percent))
        g = min(255, int(g + (255 - g) * percent))
        b = min(255, int(b + (255 - b) * percent))

        # Return the lighter color in hex format
        return f'#{r:02x}{g:02x}{b:02x}'

    def save(self, commit=True):
        instance = super().save(commit=False)
        theme_color = self.cleaned_data.get("theme_color", "#FF5733")
        card_color = self.cleaned_data.get("card_color", "#000000")

        # Update theme_settings with both theme_color and card_color
        theme_settings = instance.theme_settings or {}  # Ensure it's not None
        theme_settings["theme_color"] = theme_color
        theme_settings["card_color"] = card_color
        
        # Assign the updated theme_settings to the instance
        instance.theme_settings = theme_settings

        if commit:
            instance.save()
        return instance
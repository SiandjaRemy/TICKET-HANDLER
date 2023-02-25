from django import forms
from .models import QrInfo, Event, Profile


class CodeForm(forms.ModelForm):
    class Meta:
        model = QrInfo
        exclude = ["code", "qr_image"]

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "slug", "description", "event_image", "ticket_price", "available_tickets", "category", "stadium", "event_date_time"]
        labels = {
            "title": "Title",
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
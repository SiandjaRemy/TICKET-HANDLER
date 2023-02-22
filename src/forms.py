from django import forms
from .models import QrInfo


class CodeForm(forms.ModelForm):
    class Meta:
        model = QrInfo
        exclude = ["code", "qr_image"]


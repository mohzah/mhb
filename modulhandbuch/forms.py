from django import forms

class UploadAbbildung(forms.Form):
    file = forms.FileField()

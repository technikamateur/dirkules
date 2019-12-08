from django import forms

class SambaConfigForm(forms.Form):
    workgroup = forms.CharField(label="workgroup", max_length=11)
    server_string = forms.CharField(label="server string", max_length=15)
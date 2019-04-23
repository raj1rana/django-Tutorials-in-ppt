from django import forms
from django.core import validators



# form class
class FormName(forms.Form):
    name = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=300)
    verify_email = forms.EmailField(label='enter you email again')
    text = forms.CharField(widget=forms.Textarea)
    botcacher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

# this is for verifying email

    # validating the botcacher field with cleam methof

    # def clean_botcacher(self):
     #   botcacher = self.cleaned_data['botcacher']
     #   if len(botcacher) > 0:
     #       raise forms.ValidationError("GOTCHA !!!!")
     #   return botcacher"""




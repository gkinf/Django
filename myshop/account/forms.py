from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    # User type selection
    USER_TYPE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="User Type")

    # Optional company name field for employers
    company_name = forms.CharField(required=False, label="Company Name")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'email', 'user_type']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def clean_company_name(self):
        cd = self.cleaned_data
        if cd['user_type'] == 'employer' and not cd.get('company_name'):
            raise forms.ValidationError("Company name is required for employers.")
        return cd.get('company_name')

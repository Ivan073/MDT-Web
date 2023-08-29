from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Client, ClientData
class ClientAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')

    def get_user(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = Client.objects.get(email=email)
        if user.check_password(password):
            return user

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ClientCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Client
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'patronymic']

    def save(self, commit=True):
        user = super().save(commit=False)
        client_data = ClientData.objects.create(info='', has_child=False)
        if commit:
            user.client_data = client_data
            user.save()
        return user
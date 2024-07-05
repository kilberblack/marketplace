from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import product

class productForm(ModelForm):
    class Meta:
        model = product
        fields = '__all__'

class customUserCreation(UserCreationForm):
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('staff', 'Staff User'),
        ('superuser', 'Superuser'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    
class customUserChangeForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('staff', 'Staff User'),
        ('superuser', 'Superuser'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super(customUserChangeForm, self).__init__(*args, **kwargs)
        if self.instance.is_superuser:
            self.fields['role'].initial = 'superuser'
        elif self.instance.is_staff:
            self.fields['role'].initial = 'staff'
        else:
            self.fields['role'].initial = 'user'

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'superuser':
            user.is_staff = True
            user.is_superuser = True
        elif role == 'staff':
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False
        if commit:
            user.save()
        return user
     
class passwordChangeForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput,label="Nueva Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirme nueva Contraseña")

    class Meta:
        model = User
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Las contraseñas no son iguales")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password"])
        if commit:
            user.save()
        return user

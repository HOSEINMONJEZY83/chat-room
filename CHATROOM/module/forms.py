from django import forms
from django.core import validators
from django.http import JsonResponse

from .models import User
from django.core.exceptions import ValidationError



class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control bg-dark border-info text-info',"data-toggle":"tooltip","data-placement":"top","title":"Please Enter Valid Email","type":"email","placeholder":"email ..."}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark border border-info text-info',"type":"password","placeholder":"password ..."}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

class RegisterForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control bg-dark border border-info text-info",'placeholder':'name ...','type':'text'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    family = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control bg-dark border border-info text-info",'placeholder':'family ...','type':'text'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': "form-control bg-dark border border-info text-info",'placeholder':'email ...','type':'email',"data-toggle":"tooltip","data-placement":"top",'title':"Please Enter Valid Email"}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control bg-dark border border-info text-info",'placeholder':'password ...','type':'password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control bg-dark border border-info text-info",'placeholder':'repeat password ...','type':'password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark border border-info text-info',
                'type' : 'text',
                'placeholder' : 'name ...'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark border border-info text-info',
                'type' : 'text',
                'placeholder' : 'family ...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-dark border border-info text-info',
                'placeholder' : 'email ...',
                'data-toggle' : 'tooltip',
                'data-placement' : 'top',
                'title' : 'Please Enter Valid Email'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'type':'file',
                'accept':'.jpg, .jpeg, .png',
                'id':'file-upload'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super(EditProfileModelForm, self).__init__(*args, **kwargs)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError('The firstname field cannot be empty.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError('The lastname field cannot be empty.')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('The email field cannot be empty.')
        return email



class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control bg-dark border border-info text-info','placeholder':"password ...",'type':'password'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ],
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control bg-dark border border-info text-info','placeholder':"new password ...",'type':'password'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ],
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control bg-dark border border-info text-info','placeholder':"repeat new password ...",'type':'password'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
        ,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        oldpassword = self.cleaned_data.get('current_password')
        if not oldpassword:
            raise ValidationError('the password field must not be empty.')
        return oldpassword

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError('the new password field must not be empty.')
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if not confirm_password:
            raise ValidationError('the repeat new password field must not be empty.')
        return confirm_password

    def clean_check(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password != password:
            raise ValidationError('the new password is not same as repeating the new password!')
        return confirm_password
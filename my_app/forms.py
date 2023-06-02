from django import forms
from django.contrib.auth.forms import UserCreationForm
from my_app.models import User

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean(self):
        cleaned_data = super().clean()
        #username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        # Check if the username or email already exists
        #if User.objects.filter(username=username).exists():
        #    raise forms.ValidationError("This username is already taken.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")

        # Check if the password follows the rules
        '''password = cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must contain at least one letter.")
        '''
        return cleaned_data
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class SignupForm(forms.ModelForm):
    """
    A ModelForm for user registration, handling custom fields and password matching.
    """
    # Overriding fields to apply custom widgets for placeholder text
    full_name = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    phone_number = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    # Password fields are not part of the model's 'fields' tuple but are needed for validation
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), 
        max_length=128
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), 
        max_length=128
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number') # Note: password is handled separately in save()

    def clean(self):
        """Custom validation to ensure passwords match."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error(None, "Passwords do not match.")
            
        return cleaned_data

    def save(self, commit=True):
        """Creates and saves the user, automatically hashing the password."""
        # Use super().save(commit=False) to get the user instance without saving to DB yet
        user = super().save(commit=False)
        # Use set_password to ensure the password is hashed
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    A standard Form for authenticating users via email or phone number and password.
    """
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email or Phone Number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    
    user = None # Attribute to hold the authenticated user


    def clean(self):
        """Authenticates the user based on provided credentials."""
        cleaned_data = super().clean()
        identifier = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if identifier and password:
            try:
                # 1. Try to find the user by email
                self.user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                try:
                    # 2. Try to find the user by phone number
                    self.user = User.objects.get(phone_number=identifier)
                except User.DoesNotExist:
                    self.user = None
            
            if self.user is not None and self.user.check_password(password):
                if not self.user.is_active:
                     raise ValidationError("This account is inactive.")
                # Success: user is stored in self.user
                pass
            else:
                # Authentication failed (no user found or wrong password)
                raise ValidationError(
                    "Please enter a correct email/phone and password. Note that both fields are case-sensitive."
                )

        return cleaned_data

    def get_user(self):
        """Returns the authenticated user object."""
        return self.user

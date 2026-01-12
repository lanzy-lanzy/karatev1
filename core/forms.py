"""
Forms for user profile management and trainee operations.
"""
from django import forms
from django.contrib.auth.models import User
from core.models import UserProfile, Trainee, Registration, Judge


class TraineeProfileForm(forms.ModelForm):
    """
    Form for trainees to update their personal profile information.
    """
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth', 'profile_image']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Address',
                'rows': 3
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'type': 'date'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'accept': 'image/*'
            })
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Update the associated user's first_name, last_name, and email
        if self.cleaned_data.get('first_name'):
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name'):
            profile.user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('email'):
            profile.user.email = self.cleaned_data['email']
        
        if commit:
            profile.user.save()
            profile.save()
        return profile


class TraineeDetailForm(forms.ModelForm):
    """
    Form for trainees to update their training-specific information.
    """
    class Meta:
        model = Trainee
        fields = ['weight', 'emergency_contact', 'emergency_phone']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Weight (kg)',
                'step': '0.01'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Emergency Contact Name'
            }),
            'emergency_phone': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Emergency Contact Phone'
            })
        }


class RegistrationForm(forms.ModelForm):
    """
    Form for new member registration.
    Requires medical certificate, waiver upload, and personal information.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
            'placeholder': 'Password'
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
            'placeholder': 'Confirm Password'
        })
    )
    
    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address', 'emergency_contact', 'emergency_phone', 'belt_level', 'medical_certificate', 'waiver']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'placeholder': 'Phone Number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'type': 'date'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'placeholder': 'Address',
                'rows': 2
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'placeholder': 'Emergency Contact Name'
            }),
            'emergency_phone': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'placeholder': 'Emergency Contact Phone'
            }),
            'belt_level': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200'
            }),
            'medical_certificate': forms.FileInput(attrs={
                'class': 'block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
            'waiver': forms.FileInput(attrs={
                'class': 'block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition duration-200',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def save(self, commit=True):
        registration = super().save(commit=False)
        
        # Create user account
        if not registration.user_id:
            base_username = registration.email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
                
            user = User.objects.create_user(
                username=username,
                email=registration.email,
                password=self.cleaned_data['password'],
                first_name=registration.first_name,
                last_name=registration.last_name
            )
            registration.user = user
        
        if commit:
            registration.save()
        
        return registration


class JudgeProfileForm(forms.ModelForm):
    """
    Form for judges to update their personal profile information.
    """
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth', 'profile_image']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Address',
                'rows': 3
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'type': 'date'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'accept': 'image/*'
            })
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Update the associated user's first_name, last_name, and email
        if self.cleaned_data.get('first_name'):
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name'):
            profile.user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('email'):
            profile.user.email = self.cleaned_data['email']
        
        if commit:
            profile.user.save()
            profile.save()
        return profile

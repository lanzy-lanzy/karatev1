"""
Forms for user profile management and trainee operations.
"""
from django import forms
from django.contrib.auth.models import User
from core.models import UserProfile, Trainee


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

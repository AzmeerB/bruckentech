from django import forms
from .models import MentorApplication


class MentorApplicationForm(forms.ModelForm):
    class Meta:
        model = MentorApplication
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:border-primary'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:border-primary'
            }),
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-4 py-3 focus:outline-none focus:border-primary'}),
        }

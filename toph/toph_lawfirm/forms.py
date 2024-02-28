from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = (
            'form_id',
            'council', 'subject_land_address',
            'contact', 'contact_role',
            'contact_postal_address', 'contact_number',
            'contact_email', 'created_date',
            'last_updated','document',
        )

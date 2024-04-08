from django import forms
from .models import Entry, LawFirmCouncil

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        exclude = ['law_firm', 'status', 'council']

class EditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        exclude = ['law_firm', 'council']

class LawFirmCouncilForm(forms.ModelForm):
    class Meta:
        model = LawFirmCouncil
        fields = '__all__'
        exclude = ['law_firm', 'council']


from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
        exclude = ['entry']

from .models import Party

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = '__all__'
        exclude = ['entry']

from .models import Lodge

class LodgeForm(forms.ModelForm):
    class Meta:
        model = Lodge
        fields = ['dealing_number']

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['status', 'comment', 'document']
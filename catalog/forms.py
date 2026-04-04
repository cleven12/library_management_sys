from django import forms
from .models import Review, ReadingList

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['name', 'description', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False)
    genre = forms.ChoiceField(choices=[], required=False)
    language = forms.ChoiceField(choices=[], required=False)
    sort_by = forms.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('rating', 'Rating'),
            ('newest', 'Newest'),
        ],
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        from .models import Genre, Book
        super().__init__(*args, **kwargs)
        self.fields['genre'].choices = [('', 'All Genres')] + [
            (g.id, g.name) for g in Genre.objects.all()
        ]
        self.fields['language'].choices = [('', 'All Languages')] + Book.LANGUAGE_CHOICES

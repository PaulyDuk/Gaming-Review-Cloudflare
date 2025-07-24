from django import forms
from .models import Comment, UserReview


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4
            })
        }


class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ('rating', 'review_text')
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about this game...',
                'rows': 4
            })
        }

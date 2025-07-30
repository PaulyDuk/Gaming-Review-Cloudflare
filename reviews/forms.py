from django import forms
from .models import UserComment, UserReview


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ('body',)
        labels = {
            'body': 'Comment',
        }
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
        labels = {
            'review_text': 'Review',
        }
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

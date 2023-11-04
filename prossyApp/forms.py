from django import forms
from prossyApp.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Leave a comment"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
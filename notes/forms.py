from django.forms import ModelForm
from . import models
from django import forms


class NoteForm(ModelForm):
    class Meta:
        model = models.Note
        fields = ['title','content', 'category']
        

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows' : 6,
                'placeholder': 'Write your note...'
            }),
            'category':forms.Select(attrs={
                'class' : 'form-select'
            }),
        }

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['category'].queryset = models.Category.objects.filter(author = user)


class CategoryForm(ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']